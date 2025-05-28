from django.urls import path
from . import views

urlpatterns = [
    # 전체 시/도 목록
    path('cities/', views.get_cities, name='city-list'),
    # 특정 시/도의 구/군 목록
    path('cities/<int:city_id>/districts/', views.get_districts, name='district-list'),
] 