# users/urls.py

from django.urls import path
from .views import SignUpView, MyPageView, MyPagePutView, CheckUserIdView, CheckNicknameView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mypage/', MyPageView.as_view()),
    path('mypage/update/', MyPagePutView.as_view(), name='mypage_put_update'),
    path('check-id/', CheckUserIdView.as_view(), name='check_userid'),
    path('check-nickname/', CheckNicknameView.as_view(), name='check_nickname'),
]
