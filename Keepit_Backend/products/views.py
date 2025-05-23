# products/views.py
from rest_framework import generics
from .models import Product
from .serializers import SavingsSerializer, StockSerializer, ETFSerializer

import os
import requests
from django.http import JsonResponse
from dotenv import load_dotenv

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .external_fetch import fetch_products, fetch_stock_by_code, fetch_stock_detail_by_code, fetch_etf_by_code
from products.utils.stock_code_loader import load_top_stock_codes, load_stock_name_map, load_top_etf_codes, load_etf_name_map
from .external_fetch import fetch_products

class SavingsListAPIView(generics.ListAPIView):
    serializer_class = SavingsSerializer
    def get_queryset(self):
        return Product.objects.filter(type='saving')
    
class DepositListAPIView(generics.ListAPIView):
    serializer_class = SavingsSerializer
    def get_queryset(self):
        return Product.objects.filter(type='deposit')


class StockListAPIView(generics.ListAPIView):
    serializer_class = StockSerializer
    def get_queryset(self):
        return Product.objects.filter(type='stock')


class ETFListAPIView(generics.ListAPIView):
    serializer_class = ETFSerializer
    def get_queryset(self):
        return Product.objects.filter(type='etf')

# 금, 은 시세 불러오기
GOLDAPI_KEY = os.getenv("GOLD_API_KEY")
def metal_prices(request):
    headers = {
        'x-access-token': GOLDAPI_KEY,
        'Content-Type': 'application/json'
    }

    gold_res = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
    silver_res = requests.get('https://www.goldapi.io/api/XAG/USD', headers=headers)

    if gold_res.status_code == 200 and silver_res.status_code == 200:
        return JsonResponse({
            'gold': gold_res.json(),
            'silver': silver_res.json()
        })
    else:
        return JsonResponse({'error': '금/은 시세 조회 실패'}, status=500)
    
'''-------------------------------------------------------------------------------------------------'''

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

load_dotenv()  
API_KEY = os.getenv("FSS_API_KEY")

API_URLS = {
    'deposit': 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json',
    'saving': 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json',
}

def fetch_products(product_type):
    url = API_URLS[product_type]
    page = 1
    result = []

    while True:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': page,
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            break

        json_data = res.json().get('result', {})
        base_list = json_data.get('baseList', [])
        option_list = json_data.get('optionList', [])

        # optionList를 상품코드 기준으로 그룹핑
        option_map = {}
        for opt in option_list:
            code = (opt['fin_co_no'], opt['fin_prdt_cd'])
            if code not in option_map:
                option_map[code] = []
            option_map[code].append(opt)

        for base in base_list:
            code = (base['fin_co_no'], base['fin_prdt_cd'])
            options = option_map.get(code, [])

            for opt in options:
                result.append({
                    'name': base.get('fin_prdt_nm'),
                    'company': base.get('kor_co_nm'),
                    'link': base.get('join_link', ''),
                    'interest_rate': safe_float(opt.get('intr_rate')),
                    'special_rate': safe_float(opt.get('intr_rate2')),
                    'term': safe_int(opt.get('save_trm')),
                    'target': base.get('join_member'),
                })

        if not base_list:
            break

        page += 1

    return result


@api_view(['GET'])
def live_deposit_products(request):
    data = fetch_products('deposit')
    return Response(data)


@api_view(['GET'])
def live_saving_products(request):
    data = fetch_products('saving')
    return Response(data)

@api_view(['GET'])
def stock_list(request):
    codes = load_top_stock_codes()
    name_map = load_stock_name_map()

    result = []
    for code in codes:
        data = fetch_stock_by_code(code)
        if data:
            data['name'] = name_map.get(code, None)
            result.append(data)

    return Response(result)

@api_view(['GET'])
def etf_list(request):
    codes = load_top_etf_codes()
    name_map = load_etf_name_map()
    
    result = []
    for code in codes:
        data = fetch_etf_by_code(code)
        if data and data.get("current_price") is not None:
            data["name"] = name_map.get(code, None)
            result.append(data)
            
    return Response(result)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def stock_detail(request, stock_code):
    data = fetch_stock_detail_by_code(stock_code)
    return Response(data)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, type, identifier):
    user = request.user

    if type not in ['stock', 'deposit', 'saving', 'etf','goods']:
        return Response({'error': '유효하지 않은 상품 유형입니다.'}, status=400)

    if request.method == 'POST':
        Favorite.objects.get_or_create(user=user, type=type, identifier=identifier)
        return Response({'message': '찜 등록 완료'})

    elif request.method == 'DELETE':
        fav = Favorite.objects.filter(user=user, type=type, identifier=identifier).first()
        if fav:
            fav.delete()
            return Response({'message': '찜 해제 완료'})
        return Response({'error': '해당 찜이 존재하지 않습니다.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    result = []

    for fav in favorites:
        if fav.type == 'stock':
            stock_info = fetch_stock_by_code(fav.identifier)
            if stock_info:
                stock_info['type'] = 'stock'
                result.append(stock_info)

        elif fav.type in ['deposit', 'saving']:
            products = fetch_products(fav.type)
            item = next((p for p in products if p['name'] + p['company'] == fav.identifier), None)
            if item:
                item['type'] = fav.type
                result.append(item)

    return Response(result)

'''

@api_view(['GET'])
def savings_list(request):
    products = Product.objects.filter(type__in=['deposit', 'saving'])
    serializer = SavingsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stocks_list(request):
    products = Product.objects.filter(type='stock')
    serializer = StockSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def etf_list(request):
    products = Product.objects.filter(type='etf')
    serializer = StockSerializer(products, many=True)  # ETF 전용 serializer 따로 만들 수도 있음
    return Response(serializer.data)

@api_view(['GET'])
def goods_list(request):
    products = Product.objects.filter(type='goods')
    # TODO: GoodsSerializer 만들기
    serializer = StockSerializer(products, many=True)  # 임시로 StockSerializer 사용
    return Response(serializer.data)

'''