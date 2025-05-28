from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Bank
from .serializers import BankSerializer
from regions.models import RegionCity, RegionDistrict
import requests
from django.conf import settings

# Create your views here.

class BankViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BankSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Bank.objects.all()
        
        # 지역 필터링
        city = self.request.query_params.get('city', None)
        district = self.request.query_params.get('district', None)
        
        if city:
            queryset = queryset.filter(region_city__name=city)
        if district:
            queryset = queryset.filter(region_district__name=district)
            
        return queryset

    @action(detail=False, methods=['get'])
    def user_location(self, request):
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다.'}, status=401)
            
        user = request.user
        if not (user.region_city and user.region_district):
            return Response({'error': '사용자의 지역 정보가 설정되어 있지 않습니다.'}, status=400)
            
        banks = Bank.objects.filter(
            region_city=user.region_city,
            region_district=user.region_district
        )
        
        serializer = self.get_serializer(banks, many=True)
        return Response({
            'city': user.region_city.name,
            'district': user.region_district.name,
            'banks': serializer.data
        })

    @action(detail=False, methods=['get'])
    def search_by_location(self, request):
        city = request.query_params.get('city')
        district = request.query_params.get('district')
        
        if not city or not district:
            return Response({'error': '도시와 구/군 정보가 필요합니다.'}, status=400)
            
        city_obj = get_object_or_404(RegionCity, name=city)
        district_obj = get_object_or_404(RegionDistrict, city=city_obj, name=district)
        
        banks = Bank.objects.filter(
            region_city=city_obj,
            region_district=district_obj
        )
        
        serializer = self.get_serializer(banks, many=True)
        return Response({
            'city': city,
            'district': district,
            'banks': serializer.data
        })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_banks(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({'error': '검색어를 입력해주세요.'}, status=400)

    # 카카오맵 API 호출
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }
    
    # 카테고리로 은행 검색 (은행 카테고리 코드: BK5)
    params = {
        'category_group_code': 'BK5',
        'query': query,
        'size': 15
    }
    
    response = requests.get(
        'https://dapi.kakao.com/v2/local/search/keyword.json',
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        return Response({'error': '검색 중 오류가 발생했습니다.'}, status=response.status_code)
        
    return Response(response.json())

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_banks_by_location(request):
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    
    if not (latitude and longitude):
        return Response({'error': '위도와 경도가 필요합니다.'}, status=400)

    # 카카오맵 API 호출
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }
    
    # 주변 은행 검색 (반경 1km 이내)
    params = {
        'category_group_code': 'BK5',
        'x': longitude,
        'y': latitude,
        'radius': 1000,
        'size': 15
    }
    
    response = requests.get(
        'https://dapi.kakao.com/v2/local/search/category.json',
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        return Response({'error': '검색 중 오류가 발생했습니다.'}, status=response.status_code)
        
    return Response(response.json())

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def get_location_info(request):
    if request.method == 'GET':
        """전체 지역 목록과 로그인한 사용자의 지역 정보를 반환"""
        # 전체 지역 목록 가져오기
        cities = RegionCity.objects.all().order_by('name')
        regions_data = {
            'regions': {},  # 전체 지역 목록
            'user_location': None  # 사용자 지역 정보 (있는 경우)
        }
        
        # 지역 목록 구성
        for city in cities:
            districts = city.districts.all().order_by('name')
            # 경기도의 경우 "시" 단위로 표시
            if city.name == "경기도":
                regions_data['regions'][city.name] = [
                    district.name.replace("시 ", "시")  # "고양시 덕양구" -> "고양시"
                    .split(" ")[0]  # 구 정보 제거
                    for district in districts
                ]
                # 중복 제거
                regions_data['regions'][city.name] = list(set(regions_data['regions'][city.name]))
            else:
                regions_data['regions'][city.name] = [district.name for district in districts]
        
        # 로그인한 사용자인 경우 사용자 지역 정보 추가
        if request.user.is_authenticated and request.user.region_city and request.user.region_district:
            user = request.user
            regions_data['user_location'] = {
                'city': user.region_city.name,
                'district': user.region_district.name
            }
        
        return Response(regions_data)
        
    elif request.method == 'POST':
        """선택된 지역의 정보를 반환"""
        city_name = request.data.get('city')
        district_name = request.data.get('district')
        
        if not city_name or not district_name:
            return Response({
                'error': '시/도와 구/군 정보가 모두 필요합니다.'
            }, status=400)
            
        try:
            city = RegionCity.objects.get(name=city_name)
            
            # 경기도의 경우 district_name에 "시"만 들어옴 (예: "고양시")
            if city.name == "경기도":
                districts = RegionDistrict.objects.filter(
                    city=city,
                    name__startswith=district_name
                )
                if not districts.exists():
                    return Response({
                        'error': '해당 지역을 찾을 수 없습니다.'
                    }, status=400)
                
                # 첫 번째 구를 기본값으로 사용
                district = districts.first()
            else:
                district = RegionDistrict.objects.get(name=district_name, city=city)
            
            # 해당 지역의 은행 정보를 반환
            # 실제 은행 정보는 프론트엔드에서 카카오맵 API를 통해 가져올 것이므로,
            # 여기서는 선택된 지역 정보만 반환
            return Response({
                'city': city.name,
                'district': district.name,
                # 경기도의 경우 시 정보만 전달
                'display_name': district_name if city.name == "경기도" else district.name
            })
            
        except (RegionCity.DoesNotExist, RegionDistrict.DoesNotExist):
            return Response({
                'error': '잘못된 지역 정보입니다.'
            }, status=400)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_regions(request):
    """시/도 및 구/군 목록을 반환합니다."""
    cities = RegionCity.objects.all()
    regions_data = {}
    
    for city in cities:
        districts = city.districts.all()  # RegionDistrict의 related_name이 'districts'로 설정되어 있어야 함
        regions_data[city.name] = [district.name for district in districts]
    
    return Response(regions_data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_districts(request):
    """특정 시/도의 구/군 목록을 반환합니다."""
    city_name = request.query_params.get('city')
    if not city_name:
        return Response({'error': '시/도 이름이 필요합니다.'}, status=400)
    
    try:
        city = RegionCity.objects.get(name=city_name)
        districts = city.districts.all()
        district_names = [district.name for district in districts]
        return Response(district_names)
    except RegionCity.DoesNotExist:
        return Response({'error': '해당 시/도를 찾을 수 없습니다.'}, status=404)
