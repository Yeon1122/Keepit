# products/serializers.py
from rest_framework import serializers
from .models import Product
from .utils.savings_detail_cal import calc_deposit_final_amount, calc_saving_final_amount

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','type', 
            'name', 'company', 'link', 
            'interest_rate', 'special_rate', 'term', 'target',
        ]

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','type', 
            'name', 'company', 'link', 
            'stock_code','current_price', 'price_change',
            'trade_volume', 'trade_value', 'market_cap'
        ]

class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','type', 
            'name', 'company', 'link', 
            'stock_code', 'market_type', 
            'current_price', 'price_change', 'sector', 'warning_info',
            'open_price', 'high_price', 'low_price', 'base_price', 'weighted_avg_price',
            'high_52w', 'high_52w_date', 'low_52w', 'low_52w_date',
            'per', 'pbr', 'eps', 'bps',
            'market_cap', 'listed_shares', 'settlement_month',
            'per_value', 'trade_volume', 'trade_value', 'foreign_ownership',
            'short_selling_allowed', 'short_selling_volume'
        ]

class ETFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','type', 
            'name', 'company', 'link', 
            'stock_code', 'market_type', 
            #'nav', 'nav_change'
        ]

'---------------------------------------------------------------------------------'

class ProductCompareSerializer(serializers.ModelSerializer):
    expected_amount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'company', 'interest_rate', 'term', 'expected_amount']

    def get_expected_amount(self, obj):
        request = self.context.get('request')
        monthly_amount = int(request.data.get('monthly_amount', 0))
        months = int(request.data.get('months', 0))

        if obj.type == 'deposit':
            total_amount = monthly_amount * months  # 예금은 한 번에 넣는다고 가정
            return calc_deposit_final_amount(total_amount, months, obj.interest_rate)

        elif obj.type == 'saving':
            return calc_saving_final_amount(monthly_amount, months, obj.interest_rate)

        return None
