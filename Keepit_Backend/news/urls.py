# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stock/<str:stock_code>/', views.get_stock_news, name='get_stock_news'),
]
