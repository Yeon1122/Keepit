from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()

# 자유게시판 URL
free_post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

free_post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# 질문게시판 URL
question_post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

question_post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # 자유게시판
    path('free/', free_post_list, {'board_type': 'free'}, name='free-post-list'),
    path('free/<int:pk>/', free_post_detail, {'board_type': 'free'}, name='free-post-detail'),
    path('free/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), {'board_type': 'free'}, name='free-post-like'),
    
    # 질문게시판
    path('question/', question_post_list, {'board_type': 'question'}, name='question-post-list'),
    path('question/<int:pk>/', question_post_detail, {'board_type': 'question'}, name='question-post-detail'),
    path('question/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), {'board_type': 'question'}, name='question-post-like'),
    
    # 댓글
    path('<str:board_type>/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('<str:board_type>/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='comment-detail'),
    path('<str:board_type>/<int:post_pk>/comments/<int:pk>/like/', 
         CommentViewSet.as_view({'post': 'like'}), 
         name='comment-like'),
] 