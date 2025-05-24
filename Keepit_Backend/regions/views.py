from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import RegionCity, RegionDistrict

# Create your views here.

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_districts(request, city_id):
    """특정 시/도의 구/군 목록을 반환합니다."""
    try:
        city = RegionCity.objects.get(id=city_id)
        districts = city.districts.all().order_by('name')
        
        # 경기도의 경우 시 단위로 처리
        if city.name == "경기도":
            district_names = [
                district.name.split(" ")[0]  # "고양시 덕양구" -> "고양시"
                for district in districts
            ]
            # 중복 제거 및 정렬
            district_names = sorted(list(set(district_names)))
        else:
            district_names = [district.name for district in districts]
            
        return Response({
            'city_name': city.name,
            'districts': district_names
        })
        
    except RegionCity.DoesNotExist:
        return Response({'error': '해당 시/도를 찾을 수 없습니다.'}, status=404)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_cities(request):
    """전체 시/도 목록을 반환합니다."""
    cities = RegionCity.objects.all().order_by('name')
    return Response({
        'cities': [
            {
                'id': city.id,
                'name': city.name
            }
            for city in cities
        ]
    })
