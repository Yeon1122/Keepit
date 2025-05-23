# products/urls.py
from django.urls import path
from . import views
from .views import metal_prices


urlpatterns = [
    path('savings/', views.live_saving_products, name='live_saving_products'),
    path('deposits/', views.live_deposit_products, name='live_deposit_products'),
    path('stocks/', views.stock_list, name='stock-list'),
    path('etfs/', views.etf_list, name='etf-list'),
    path('goods/', metal_prices),

    path('stocks/<str:stock_code>/', views.stock_detail, name='stock-detail'),

    # path('favorites/', views.my_favorites, name='my-favorites'), -> users로 이동!
     path('<str:type>/<str:identifier>/favorite/', views.toggle_favorite, name='toggle-favorite'),

    # path('goods/', GoodsListAPIView.as_view(), name='goods-list'),
    # path('fetch-all-products/', views.fetch_all_deposit_saving, name='fetch-all-products'),
    # path('savings/', views.savings_list, name='savings-list'),
    # path('stocks/', views.stocks_list, name='stocks-list'),
    # path('etf/', views.etf_list, name='etf-list'),
    # path('goods/', views.goods_list, name='goods-list'),
]
