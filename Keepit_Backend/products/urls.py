# products/urls.py
from django.urls import path
from .views import (
    SavingsListAPIView, StockListAPIView, ETFListAPIView, # GoodsListAPIView,
)

urlpatterns = [
    path('savings/', SavingsListAPIView.as_view(), name='savings-list'),
    path('stocks/', StockListAPIView.as_view(), name='stock-list'),
    path('etf/', ETFListAPIView.as_view(), name='etf-list'),
    # path('goods/', GoodsListAPIView.as_view(), name='goods-list'),
]
