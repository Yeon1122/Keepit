from django.urls import path
from . import views

urlpatterns = [
    # 지역 정보 조회 (로그인 사용자: 자동 지역 정보, 비로그인: 전체 지역 목록)
    path('nearby/', views.get_location_info, name='location-info'),
] 