from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Count

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.action == 'list':  # 목록 조회
            permission_classes = [permissions.AllowAny]
        else:  # 상세 조회, 생성, 수정, 삭제, 좋아요 등 다른 모든 동작
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        board_type = self.kwargs.get('board_type')
        return Post.objects.filter(board_type=board_type)

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
    permission_classes = [permissions.IsAuthenticated]  # 댓글은 모든 동작에 로그인 필요

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
