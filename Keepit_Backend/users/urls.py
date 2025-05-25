# users/urls.py

from django.urls import path
from .views import (
    SignUpView, CustomAuthToken, MyPageView, UserDetailView,
    CheckUserIdView, CheckNicknameView, LogoutView,
    FollowToggleView, FollowListView)
from products.views import user_favorites

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='token_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('mypage/', MyPageView.as_view()),
    path('favorites/', user_favorites, name='user-favorites'),  # 현재 사용자의 찜 목록
    path('favorites/<str:userid>/', user_favorites, name='user-favorites-detail'),  # 특정 사용자의 찜 목록

    path('follow-info/<str:userid>/', FollowListView.as_view(), name='follow_info'),
    path('<str:userid>/follow/', FollowToggleView.as_view(), name='follow_toggle'),
    
    path('check-id/', CheckUserIdView.as_view(), name='check_userid'),
    path('check-nickname/', CheckNicknameView.as_view(), name='check_nickname'),
    
    path('<str:userid>/', UserDetailView.as_view(), name='user_detail'),
    
    ]
