# users/urls.py

from django.urls import path
from .views import SignUpView, CustomAuthToken, MyPageView, MyPagePutView, CheckUserIdView, CheckNicknameView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='token_login'),
    path('mypage/', MyPageView.as_view()),
    path('mypage/update/', MyPagePutView.as_view(), name='mypage_put_update'),
    path('check-id/', CheckUserIdView.as_view(), name='check_userid'),
    path('check-nickname/', CheckNicknameView.as_view(), name='check_nickname'),
]
