from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.create_chat_session, name='start-chat'),  # 채팅 시작 (카테고리 선택)
    path('chat/<int:session_id>/', views.send_message, name='chat'),  # 메시지 주고받기
] 