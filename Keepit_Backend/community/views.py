from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
