from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_test_page, name='test-page'),
    path('submit/', views.submit_test, name='submit-test'),
    path('result/', views.get_test_result, name='test-result'),
    path('result/delete/', views.delete_test_result, name='delete-test-result'),
] 