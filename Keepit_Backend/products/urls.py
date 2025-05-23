# products/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('savings/', views.live_saving_products, name='live_saving_products'),
    path('deposits/', views.live_deposit_products, name='live_deposit_products'),
    # path('stocks/', StockListAPIView.as_view(), name='stock-list'),
    # path('etf/', ETFListAPIView.as_view(), name='etf-list'),
    # path('goods/', GoodsListAPIView.as_view(), name='goods-list'),
    # path('fetch-all-products/', views.fetch_all_deposit_saving, name='fetch-all-products'),
    # path('savings/', views.savings_list, name='savings-list'),
    # path('stocks/', views.stocks_list, name='stocks-list'),
    # path('etf/', views.etf_list, name='etf-list'),
    # path('goods/', views.goods_list, name='goods-list'),
]
