# products/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('savings/', views.live_saving_products, name='live_saving_products'),
    path('deposits/', views.live_deposit_products, name='live_deposit_products'),
    path('stocks/', views.stock_list, name='stock-list'),
    path('etfs/', views.etf_list, name='etf-list'),
    path('goods/', views.metal_prices),

    path('stocks/<str:stock_code>/', views.stock_detail, name='stock-detail'),

    # path('favorites/', views.my_favorites, name='my-favorites'), -> users로 이동!
    path('<str:type>/<str:identifier>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('deposit/compare/', views.compare_deposits, name='compare-deposits'),
    path('saving/compare/', views.compare_savings, name='compare-savings'),
]