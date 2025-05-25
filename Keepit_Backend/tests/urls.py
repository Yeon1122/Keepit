from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_test_page, name='test_page'),
    path('submit/', views.submit_test, name='submit_test'),
    path('result/', views.get_test_result, name='get_test_result'),
    path('result/<str:userid>/', views.get_user_test_result, name='get_user_test_result'),
    path('result/delete/', views.delete_test_result, name='delete_test_result'),
] 