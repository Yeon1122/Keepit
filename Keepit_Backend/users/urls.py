# users/urls.py

from django.urls import path
from .views import SignUpView, MyPageView, MyPagePutView
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
]
