# products/urls.py
from django.urls import path
from . import views
from .views import (
    SavingsListAPIView, SavingsDetailAPIView,
    DepositListAPIView, DepositDetailAPIView,
)

urlpatterns = [
    # 예금/적금 상품 목록
    path('deposits/', DepositListAPIView.as_view(), name='deposit-list'),
    path('savings/', SavingsListAPIView.as_view(), name='savings-list'),
    path('savings/<int:pk>/', SavingsDetailAPIView.as_view(), name='savings-detail'),
    path('deposits/<int:pk>/', DepositDetailAPIView.as_view(), name='deposit-detail'),
    
    # 외부 API 데이터 가져오기
    path('fetch-deposits/', views.fetch_deposit_products, name='fetch-deposits'),
    path('fetch-savings/', views.fetch_saving_products, name='fetch-savings'),
    
    # 주식/ETF 관련
    path('stocks/', views.stock_list, name='stock-list'),
    path('etfs/', views.etf_list, name='etf-list'),
    path('stocks/<str:stock_code>/', views.stock_detail, name='stock-detail'),
    path('stocks/<str:stock_code>/favorite/', views.stock_favorite, name='stock-favorite'),
    path('etfs/<str:etf_code>/favorite/', views.etf_favorite, name='etf-favorite'),
    
    # 현물 관련
    path('goods/', views.goods_list, name='goods-list'),
    path('goods/<int:goods_id>/favorite/', views.goods_favorite, name='goods-favorite'),
    
    # 찜하기 기능
    path('favorites/by-id/<int:product_id>/', views.favorite_by_id, name='favorite-by-id'),
    path('favorites/', views.user_favorites, name='user-favorites'),
    path('favorites/<str:userid>/', views.user_favorites, name='user-favorites-detail'),
    
    # 상품 비교
    path('compare/deposits/', views.compare_deposits, name='compare-deposits'),
    path('compare/savings/', views.compare_savings, name='compare-savings'),
]