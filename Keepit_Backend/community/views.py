from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Count

User = get_user_model()

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':  # 목록 조회와 상세 조회는 모두 가능
            permission_classes = [permissions.AllowAny]
        else:  # 생성, 수정, 삭제, 좋아요 등은 로그인 필요
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        board_type = self.kwargs.get('board_type')
        return Post.objects.filter(board_type=board_type)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'id': post.id,
            'board_type': post.board_type,
            'message': '게시글이 성공적으로 생성되었습니다.',
            'author_id': post.author.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print("Current user:", self.request.user)  # 디버깅용
        print("Is user authenticated:", self.request.user.is_authenticated)  # 디버깅용
        print("Board type:", self.kwargs.get('board_type'))  # 디버깅용
        post = serializer.save(
            author=self.request.user,
            board_type=self.kwargs.get('board_type')
        )
        print("Created post author:", post.author)  # 디버깅용
        return post

    def perform_update(self, serializer):
        post = self.get_object()
        print(f"Updating post - Current user: {self.request.user.userid}, Post author: {post.author.userid}")  # 디버깅용
        if str(post.author.userid) != str(self.request.user.userid):
            raise permissions.PermissionDenied("자신의 게시글만 수정할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        print(f"Deleting post - Current user: {self.request.user.userid}, Post author: {instance.author.userid}")  # 디버깅용
        if str(instance.author.userid) != str(self.request.user.userid):
            raise permissions.PermissionDenied("자신의 게시글만 삭제할 수 있습니다.")
        instance.delete()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None, board_type=None):
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            post.likes.add(user)
            return Response({'status': 'liked'})

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # 댓글 조회는 누구나 가능
            permission_classes = [permissions.AllowAny]
        else:  # 생성, 수정, 삭제, 좋아요 등은 로그인 필요
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None, post_pk=None, **kwargs):
        comment = self.get_object()
        user = request.user
        
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            comment.likes.add(user)
            return Response({'status': 'liked'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_posts(request):
    """사용자가 작성한 게시글 목록을 반환합니다."""
    posts = Post.objects.filter(author=request.user).select_related('author').prefetch_related('likes', 'comments')
    
    # 게시판 별 게시글 수 계산
    posts_by_type = posts.values('board_type').annotate(count=Count('id'))
    posts_count = {
        'free': 0,
        'question': 0
    }
    for item in posts_by_type:
        posts_count[item['board_type']] = item['count']
    
    # 게시글 목록 직렬화
    serializer = PostSerializer(posts, many=True)
    
    return Response({
        'total_posts': posts.count(),
        'posts_count': posts_count,
        'posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_posts(request, userid):
    """특정 사용자가 작성한 게시글 목록을 반환합니다."""
    try:
        user = get_object_or_404(User, userid=userid)
        posts = Post.objects.filter(author=user).select_related('author').prefetch_related('likes', 'comments')
        
        # 게시판 별 게시글 수 계산
        posts_by_type = posts.values('board_type').annotate(count=Count('id'))
        posts_count = {
            'free': 0,
            'question': 0
        }
        for item in posts_by_type:
            posts_count[item['board_type']] = item['count']
        
        # 게시글 목록 직렬화
        serializer = PostSerializer(posts, many=True, context={'request': request})
        
        return Response({
            'total_posts': posts.count(),
            'posts_count': posts_count,
            'posts': serializer.data,
            'author': {
                'userid': user.userid,
                'nickname': user.nickname
            }
        })
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)
