# products/views.py
from rest_framework import generics
from .models import Product
from .serializers import SavingsSerializer, StockSerializer, ETFSerializer

class SavingsListAPIView(generics.ListAPIView):
    serializer_class = SavingsSerializer

    def get_queryset(self):
        return Product.objects.filter(type__in=['deposit', 'saving'])


class StockListAPIView(generics.ListAPIView):
    serializer_class = StockSerializer

    def get_queryset(self):
        return Product.objects.filter(type='stock')


class ETFListAPIView(generics.ListAPIView):
    serializer_class = ETFSerializer

    def get_queryset(self):
        return Product.objects.filter(type='etf')


# from .serializers import ProductSerializer  # 공통 serializer

# class GoodsListAPIView(generics.ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         return Product.objects.filter(type='goods')
