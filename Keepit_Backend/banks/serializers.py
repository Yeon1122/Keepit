from rest_framework import serializers
from .models import Bank
from regions.models import RegionCity, RegionDistrict

class BankSerializer(serializers.ModelSerializer):
    bank_type_display = serializers.CharField(source='get_bank_type_display', read_only=True)
    region_city_name = serializers.CharField(source='region_city.name', read_only=True)
    region_district_name = serializers.CharField(source='region_district.name', read_only=True)

    class Meta:
        model = Bank
        fields = ['id', 'name', 'bank_type', 'bank_type_display', 'address', 
                 'region_city', 'region_city_name', 'region_district', 'region_district_name',
                 'latitude', 'longitude', 'phone', 'operating_hours']
        read_only_fields = ['bank_type_display', 'region_city_name', 'region_district_name'] 