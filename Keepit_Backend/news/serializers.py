# news/serializers.py
from rest_framework import serializers
from .models import StockNews

class StockNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockNews
        fields = ['id', 'stock_code', 'title', 'link', 'published_at']
