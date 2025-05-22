# users/serializers.py

from rest_framework import serializers
from .models import User
from regions.models import RegionCity, RegionDistrict

class UserCreateSerializer(serializers.ModelSerializer):
    region_city_name = serializers.CharField(write_only=True)
    region_district_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'userid', 'password', 'email', 'nickname', 'name',
            'birth_year', 'birth_month', 'birth_day',
            'region_city_name', 'region_district_name'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        city_name_raw = validated_data.pop('region_city_name')
        city_name = (
            city_name_raw.replace("특별시", "")
                         .replace("광역시", "")
                         .replace("시", "")
        )
        district_name = validated_data.pop('region_district_name')

        try:
            city = RegionCity.objects.get(name__icontains=city_name)
        except RegionCity.DoesNotExist:
            raise serializers.ValidationError({'region_city_name': f'{city_name} 시는 존재하지 않습니다.'})

        try:
            district = RegionDistrict.objects.get(name=district_name, city=city)
        except RegionDistrict.DoesNotExist:
            raise serializers.ValidationError({'region_district_name': f'{district_name} 는 {city.name}에 존재하지 않습니다.'})

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.region_city = city
        user.region_district = district
        user.save()
        return user
