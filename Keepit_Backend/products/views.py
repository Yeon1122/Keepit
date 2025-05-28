# products/views.py
from rest_framework import generics, status
from .models import Product
from .serializers import SavingsSerializer, StockSerializer, ETFSerializer, ProductCompareSerializer, GoodsSerializer

import os
import requests
from django.http import JsonResponse, StreamingHttpResponse
from dotenv import load_dotenv

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .external_fetch import fetch_products, fetch_stock_by_code, fetch_stock_detail_by_code, fetch_etf_by_code, fetch_product_details_by_name
from products.utils.stock_code_loader import load_top_stock_codes, load_stock_name_map, load_top_etf_codes, load_etf_name_map
from .external_fetch import fetch_products, fetch_product_details_by_name
from .utils.savings_detail_cal import filter_one_option_per_product, calc_saving_final_amount, calc_deposit_final_amount
from django.conf import settings

import logging
import json
import time
from users.models import User

logger = logging.getLogger(__name__)

class SavingsListAPIView(generics.ListAPIView):
    serializer_class = SavingsSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(type='saving')
        count = queryset.count()
        logger.info(f"[SavingsListAPIView] Found {count} saving products in DB")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # DB에 데이터가 없으면 외부 API에서 가져오기
        if not queryset.exists():
            logger.info("[SavingsListAPIView] DB empty, fetching from external API")
            try:
                # 외부 API에서 데이터 가져오기
                data = fetch_products('saving')
                logger.info(f"[SavingsListAPIView] Fetched {len(data)} products from external API")
                
                # DB에 저장
                saved_count = 0
                for product_data in data:
                    try:
                        Product.objects.update_or_create(
                            type='saving',
                            name=product_data['fin_prdt_nm'],
                            company=product_data['kor_co_nm'],
                            defaults={
                                'interest_rate': product_data['intr_rate'] or 0,
                                'special_rate': product_data['intr_rate2'] or 0,
                                'term': product_data['save_trm'] or 0,
                                'target': product_data['join_member'] or ''
                            }
                        )
                        saved_count += 1
                    except Exception as e:
                        logger.error(f"[SavingsListAPIView] Error saving product: {str(e)}")
                        continue
                
                logger.info(f"[SavingsListAPIView] Saved {saved_count} products to DB")
                
                # 저장된 데이터 다시 조회
                queryset = self.get_queryset()
            except Exception as e:
                logger.error(f"[SavingsListAPIView] Error fetching from external API: {str(e)}")
                return Response({
                    "error": "Failed to fetch products",
                    "detail": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 데이터 직렬화 및 응답
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"[SavingsListAPIView] Returning {len(serializer.data)} products")
        return Response(serializer.data)  # 배열 형태로 직접 반환

class SavingsDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(type='saving')
    serializer_class = SavingsSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f"[SavingsDetailAPIView] Retrieved saving product with id {instance.id}")
        return Response(serializer.data)

class DepositListAPIView(generics.ListAPIView):
    serializer_class = SavingsSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(type='deposit')
        count = queryset.count()
        logger.info(f"[DepositListAPIView] Found {count} deposit products in DB")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # DB에 데이터가 없으면 외부 API에서 가져오기
        if not queryset.exists():
            logger.info("[DepositListAPIView] DB empty, fetching from external API")
            try:
                # 외부 API에서 데이터 가져오기
                data = fetch_products('deposit')
                logger.info(f"[DepositListAPIView] Fetched {len(data)} products from external API")
                
                # DB에 저장
                saved_count = 0
                for product_data in data:
                    try:
                        Product.objects.update_or_create(
                            type='deposit',
                            name=product_data['fin_prdt_nm'],
                            company=product_data['kor_co_nm'],
                            defaults={
                                'interest_rate': product_data['intr_rate'] or 0,
                                'special_rate': product_data['intr_rate2'] or 0,
                                'term': product_data['save_trm'] or 0,
                                'target': product_data['join_member'] or ''
                            }
                        )
                        saved_count += 1
                    except Exception as e:
                        logger.error(f"[DepositListAPIView] Error saving product: {str(e)}")
                        continue
                
                logger.info(f"[DepositListAPIView] Saved {saved_count} products to DB")
                
                # 저장된 데이터 다시 조회
                queryset = self.get_queryset()
            except Exception as e:
                logger.error(f"[DepositListAPIView] Error fetching from external API: {str(e)}")
                return Response({
                    "error": "Failed to fetch products",
                    "detail": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 데이터 직렬화 및 응답
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"[DepositListAPIView] Returning {len(serializer.data)} products")
        return Response(serializer.data)  # 배열 형태로 직접 반환

class DepositDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(type='deposit')
    serializer_class = SavingsSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f"[DepositDetailAPIView] Retrieved deposit product with id {instance.id}")
        return Response(serializer.data)

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

    logger.info(f"[fetch_products] Fetching {product_type} products from external API")
    while True:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': page,
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            logger.error(f"[fetch_products] API request failed: {res.status_code}")
            break

        json_data = res.json().get('result', {})
        base_list = json_data.get('baseList', [])
        option_list = json_data.get('optionList', [])

        if not base_list:
            break

        logger.info(f"[fetch_products] Page {page}: Found {len(base_list)} base products and {len(option_list)} options")

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
                    'fin_prdt_nm': base.get('fin_prdt_nm'),
                    'kor_co_nm': base.get('kor_co_nm'),
                    'join_member': base.get('join_member', ''),
                    'intr_rate': safe_float(opt.get('intr_rate')),
                    'intr_rate2': safe_float(opt.get('intr_rate2')),
                    'save_trm': safe_int(opt.get('save_trm')),
                })

        page += 1

    logger.info(f"[fetch_products] Total {len(result)} products fetched from external API")
    return result


@api_view(['GET'])
def fetch_deposit_products(request):
    """외부 API에서 예금 상품을 가져와서 DB에 저장"""
    try:
        data = fetch_products('deposit')
        logger.info(f"[fetch_deposit_products] Fetched {len(data)} deposit products from external API")
        
        saved_count = 0
        for product_data in data:
            try:
                Product.objects.update_or_create(
                    type='deposit',
                    name=product_data['fin_prdt_nm'],
                    company=product_data['kor_co_nm'],
                    defaults={
                        'interest_rate': product_data['intr_rate'] or 0,
                        'special_rate': product_data['intr_rate2'] or 0,
                        'term': product_data['save_trm'] or 0,
                        'target': product_data['join_member'] or ''
                    }
                )
                saved_count += 1
            except Exception as e:
                logger.error(f"[fetch_deposit_products] Error saving product: {str(e)}")
                continue
        
        logger.info(f"[fetch_deposit_products] Successfully saved {saved_count} deposit products to DB")
        return Response({
            "message": f"Successfully fetched and saved {saved_count} deposit products",
            "total_fetched": len(data),
            "source": "external_api",
            "status": "completed"
        })
    except Exception as e:
        logger.error(f"[fetch_deposit_products] Error: {str(e)}")
        return Response({
            "error": "Failed to fetch deposit products",
            "source": "external_api",
            "status": "failed"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_saving_products(request):
    """외부 API에서 적금 상품을 가져와서 DB에 저장"""
    try:
        data = fetch_products('saving')
        logger.info(f"[fetch_saving_products] Fetched {len(data)} saving products from external API")
        
        saved_count = 0
        for product_data in data:
            try:
                Product.objects.update_or_create(
                    type='saving',
                    name=product_data['fin_prdt_nm'],
                    company=product_data['kor_co_nm'],
                    defaults={
                        'interest_rate': product_data['intr_rate'] or 0,
                        'special_rate': product_data['intr_rate2'] or 0,
                        'term': product_data['save_trm'] or 0,
                        'target': product_data['join_member'] or ''
                    }
                )
                saved_count += 1
            except Exception as e:
                logger.error(f"[fetch_saving_products] Error saving product: {str(e)}")
                continue
        
        logger.info(f"[fetch_saving_products] Successfully saved {saved_count} saving products to DB")
        return Response({
            "message": f"Successfully fetched and saved {saved_count} saving products",
            "total_fetched": len(data),
            "source": "external_api",
            "status": "completed"
        })
    except Exception as e:
        logger.error(f"[fetch_saving_products] Error: {str(e)}")
        return Response({
            "error": "Failed to fetch saving products",
            "source": "external_api",
            "status": "failed"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def stock_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 50))
    
    codes = load_top_stock_codes()
    name_map = load_stock_name_map()
    
    # 페이지네이션 적용
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    current_codes = codes[start_idx:end_idx]
    
    # 현재 사용자의 찜하기 목록 가져오기
    user_favorites = set()
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(
            user=request.user,
            type='stock'
        ).values_list('identifier', flat=True)
        # 작은따옴표가 있든 없든 동일한 코드로 처리
        user_favorites = {fav.replace("'", "") for fav in favorites}
    
    result = []
    for code in current_codes:
        # 코드에서 작은따옴표 제거
        clean_code = code.replace("'", "")
        data = fetch_stock_by_code(clean_code)
        if data:
            # 네이버 크롤링 데이터에서 이름 가져오기
            stock_name = name_map.get(clean_code)
            
            # 크롤링 데이터에 없으면 API 응답에서 가져오기
            if not stock_name:
                stock_name = data.get('hts_kor_isnm')
                
            # 둘 다 없으면 코드 사용
            if not stock_name:
                stock_name = clean_code
                
            data.update({
                'name': stock_name,
                'is_liked': clean_code in user_favorites
            })
            result.append(data)
            
    return Response({
        'data': result,
        'has_more': end_idx < len(codes),
        'total_count': len(codes),
        'current_page': page
    })

@api_view(['GET'])
def etf_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 100))
    
    codes = load_top_etf_codes()
    name_map = load_etf_name_map()
    
    # 페이지네이션 적용
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    current_codes = codes[start_idx:end_idx]
    
    # 현재 사용자의 찜하기 목록 가져오기
    user_favorites = set()
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(
            user=request.user,
            type='etf'
        ).values_list('identifier', flat=True)
        user_favorites = {fav.replace("'", "") for fav in favorites}
    
    result = []
    for code in current_codes:
        clean_code = code.replace("'", "")
        data = fetch_etf_by_code(clean_code)
        if data and data.get("current_price") is not None:
            # 네이버 크롤링 데이터에서 이름 가져오기
            etf_name = name_map.get(clean_code)
            
            # 크롤링 데이터에 없으면 API 응답에서 가져오기
            if not etf_name:
                etf_name = data.get('hts_kor_isnm')
                
            # 둘 다 없으면 코드 사용
            if not etf_name:
                etf_name = clean_code
                
            data.update({
                'name': etf_name,
                'is_liked': clean_code in user_favorites
            })
            result.append(data)
            
    return Response({
        'data': result,
        'has_more': end_idx < len(codes),
        'total_count': len(codes),
        'current_page': page
    })

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def stock_detail(request, stock_code):
    data = fetch_stock_detail_by_code(stock_code)
    return Response(data)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_by_id(request, product_id):
    """
    상품 ID를 기반으로 찜하기/찜해제 토글 API
    """
    try:
        user = request.user
        print(f"[favorite_by_id] User {user.id} trying to toggle favorite for product {product_id}")

        # 상품 존재 여부 확인
        product = Product.objects.filter(id=product_id).first()
        if not product:
            print(f"[favorite_by_id] Product not found: {product_id}")
            return Response(
                {'error': '해당 상품을 찾을 수 없습니다.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # identifier를 product_id로 통일
        identifier = str(product_id)

        if request.method == 'GET':
            # 찜하기 상태 확인
            is_liked = Favorite.objects.filter(
                user=user,
                type=product.type,
                identifier=identifier
            ).exists()
            print(f"[favorite_by_id] Product {product_id} is {'liked' if is_liked else 'not liked'} by user {user.id}")
            return Response({
                'is_liked': is_liked
            })

        elif request.method == 'POST':
            # 찜하기 생성 또는 가져오기
            favorite, created = Favorite.objects.get_or_create(
                user=user,
                type=product.type,
                identifier=identifier
            )
            print(f"[favorite_by_id] Favorite {'created' if created else 'already exists'} for product {product_id}")
            return Response({
                'message': '찜하기가 완료되었습니다.',
                'is_liked': True
            })

        elif request.method == 'DELETE':
            # 찜하기 삭제
            result = Favorite.objects.filter(
                user=user,
                type=product.type,
                identifier=identifier
            ).delete()
            
            if result[0] > 0:  # 삭제된 항목이 있는 경우
                print(f"[favorite_by_id] Favorite removed for product {product_id}")
                return Response({
                    'message': '찜하기가 해제되었습니다.',
                    'is_liked': False
                })
            print(f"[favorite_by_id] Favorite not found for product {product_id}")
            return Response(
                {'error': '해당 찜하기가 존재하지 않습니다.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"[favorite_by_id] Error: {str(e)}")
        return Response(
            {'error': '찜하기 처리 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favorites(request, userid=None):
    try:
        # userid가 주어진 경우 해당 사용자의 찜 목록을, 아니면 현재 로그인한 사용자의 찜 목록을 가져옴
        target_user = User.objects.get(userid=userid) if userid else request.user
        favorites = Favorite.objects.filter(user=target_user)
        
        liked_products = []
        for fav in favorites:
            try:
                if fav.type in ['deposit', 'saving']:
                    # 예금/적금 상품은 product_id로 조회
                    product_id = int(fav.identifier)
                    product = Product.objects.filter(id=product_id).first()
                    
                    if product:
                        product_data = {
                            'id': product.id,
                            'type': product.type,
                            'name': product.name,
                            'company': product.company,
                            'interest_rate': product.interest_rate,
                            'special_rate': product.special_rate,
                            'term': product.term,
                            'target': product.target,
                            'is_liked': True
                        }
                        liked_products.append(product_data)
                        
                elif fav.type == 'stock':
                    # 주식은 실시간 API로 조회
                    stock_code = fav.identifier.replace("'", "")
                    name_map = load_stock_name_map()
                    stock_data = fetch_stock_by_code(stock_code)
                    
                    if stock_data:
                        stock_name = name_map.get(stock_code)
                        if not stock_name:
                            stock_name = stock_data.get('hts_kor_isnm')
                        if not stock_name:
                            stock_name = stock_code
                            
                        product_data = {
                            'id': f"stock_{stock_code}",
                            'type': 'stock',
                            'name': stock_name,
                            'company': stock_data.get('company', ''),
                            'product_code': stock_code,
                            'current_price': stock_data.get('current_price'),
                            'previous_price': stock_data.get('previous_price'),
                            'price_change': stock_data.get('price_change'),
                            'fluctuation_rate': stock_data.get('fluctuation_rate'),
                            'market_cap': stock_data.get('market_cap'),
                            'is_liked': True
                        }
                        liked_products.append(product_data)
                        
                elif fav.type == 'etf':
                    # ETF는 실시간 API로 조회
                    etf_code = fav.identifier.replace("'", "")
                    name_map = load_etf_name_map()
                    etf_data = fetch_etf_by_code(etf_code)
                    
                    if etf_data:
                        etf_name = name_map.get(etf_code)
                        if not etf_name:
                            etf_name = etf_data.get('hts_kor_isnm')
                        if not etf_name:
                            etf_name = etf_code
                            
                        product_data = {
                            'id': f"etf_{etf_code}",
                            'type': 'etf',
                            'name': etf_name,
                            'company': etf_data.get('company', ''),
                            'product_code': etf_code,
                            'current_price': etf_data.get('current_price'),
                            'previous_price': etf_data.get('previous_price'),
                            'price_change': etf_data.get('price_change'),
                            'fluctuation_rate': etf_data.get('fluctuation_rate'),
                            'market_cap': etf_data.get('market_cap'),
                            'is_liked': True
                        }
                        liked_products.append(product_data)
                        
                elif fav.type == 'goods':
                    # 현물은 실시간 API로 조회
                    goods_id = int(fav.identifier)
                    
                    # 현물 데이터 가져오기 (금/은)
                    try:
                        headers = {
                            'x-access-token': os.getenv("GOLD_API_KEY"),
                            'Content-Type': 'application/json'
                        }

                        if goods_id == 1:  # 금
                            gold_res = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
                            if gold_res.status_code == 200:
                                gold_data = gold_res.json()
                                product_data = {
                                    'id': 1,
                                    'type': 'goods',
                                    'name': '금 (Gold)',
                                    'company': 'GoldAPI.io',
                                    'current_price': gold_data.get('price'),
                                    'price_change': gold_data.get('ch'),
                                    'trade_volume': gold_data.get('vol'),
                                    'trade_value': gold_data.get('price_gram_24k'),
                                    'market_cap': None,
                                    'unit': 'USD per troy ounce',
                                    'is_liked': True
                                }
                                liked_products.append(product_data)
                        elif goods_id == 2:  # 은
                            silver_res = requests.get('https://www.goldapi.io/api/XAG/USD', headers=headers)
                            if silver_res.status_code == 200:
                                silver_data = silver_res.json()
                                product_data = {
                                    'id': 2,
                                    'type': 'goods',
                                    'name': '은 (Silver)',
                                    'company': 'GoldAPI.io',
                                    'current_price': silver_data.get('price'),
                                    'price_change': silver_data.get('ch'),
                                    'trade_volume': silver_data.get('vol'),
                                    'trade_value': silver_data.get('price_gram_24k'),
                                    'market_cap': None,
                                    'unit': 'USD per troy ounce',
                                    'is_liked': True
                                }
                                liked_products.append(product_data)
                    except Exception as goods_error:
                        print(f"현물 데이터 조회 중 오류: {str(goods_error)}")
                        continue

            except (ValueError, Product.DoesNotExist) as e:
                print(f"찜한 상품 처리 중 오류 발생: {str(e)}, type={fav.type}, identifier={fav.identifier}")
                continue

        return Response(liked_products)
    
    except User.DoesNotExist:
        return Response({"message": "사용자를 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return Response({"message": f"오류가 발생했습니다: {str(e)}"}, status=500)

# 예금, 적금 상세 비교
@api_view(['POST'])
def compare_deposits(request):
    return compare_products_by_name(request, 'deposit')

@api_view(['POST'])
def compare_savings(request):
    return compare_products_by_name(request, 'saving')

def compare_products_by_name(request, product_type):
    product_names = request.data.get('product_names')
    monthly_amount = int(request.data.get('monthly_amount', 0))
    months = int(request.data.get('months', 0))

    if not product_names or len(product_names) != 2:
        return Response({'error': '상품 이름 2개를 선택해야 합니다.'}, status=400)

    all_matched = fetch_product_details_by_name(product_names, product_type)

    # 각 상품별로 가능한 저축 기간 확인
    available_terms = {}
    for product in all_matched:
        name = product['name']
        if name not in available_terms:
            available_terms[name] = set()
        available_terms[name].add(product['term'])

    # 선택한 기간이 모든 상품에서 불가능한 경우 안내 메시지 반환
    invalid_products = []
    for name, terms in available_terms.items():
        if not terms or months not in terms:
            invalid_products.append({
                'name': name,
                'available_terms': sorted(list(terms))
            })
    
    if invalid_products:
        error_message = "선택하신 저축 기간이 가능하지 않은 상품이 있습니다.\n"
        for product in invalid_products:
            error_message += f"\n- {product['name']}: "
            if product['available_terms']:
                error_message += f"가능한 기간은 {', '.join(map(str, product['available_terms']))}개월입니다."
            else:
                error_message += "가능한 저축 기간 정보가 없습니다."
        return Response({'error': error_message}, status=400)

    # ✅ 여기서 중복 제거 + 원하는 기간 선택!
    matched = filter_one_option_per_product(all_matched, months)

    if len(matched) != 2:
        return Response({'error': '해당 상품 정보를 찾을 수 없습니다.'}, status=404)

    # 계산 결과 붙이기
    result = []
    for product in matched:
        # 기본금리만 사용
        interest_rate = product['interest_rate']
        
        if product_type == 'saving':
            expected = calc_saving_final_amount(monthly_amount, months, interest_rate)
        else:
            total_amount = monthly_amount
            expected = calc_deposit_final_amount(total_amount, months, interest_rate)

        result.append({
            **product,
            "expected_amount": expected
        })

    return Response({'products': result})


@api_view(['GET'])
def savings_list(request):
    try:
        # API 키 확인
        api_key = settings.FSS_API_KEY
        if not api_key:
            return Response({"error": "API key is not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 정기예금 데이터 가져오기
        deposit_url = 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        deposit_response = requests.get(deposit_url, params={
            'auth': api_key,
            'topFinGrpNo': '020000',
            'pageNo': '1'
        })
        
        if deposit_response.status_code != 200:
            print(f"Deposit API Error: {deposit_response.text}")
            return Response({"error": "Failed to fetch deposit products"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        deposit_data = deposit_response.json()
        
        # 적금 데이터 가져오기
        saving_url = 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
        saving_response = requests.get(saving_url, params={
            'auth': api_key,
            'topFinGrpNo': '020000',
            'pageNo': '1'
        })
        
        if saving_response.status_code != 200:
            print(f"Saving API Error: {saving_response.text}")
            return Response({"error": "Failed to fetch saving products"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        saving_data = saving_response.json()
        
        # 데이터 변환 및 통합
        products = []
        user = request.user
        
        # 정기예금 데이터 변환 및 저장
        if 'result' in deposit_data and 'baseList' in deposit_data['result']:
            for base_item in deposit_data['result']['baseList']:
                options = deposit_data['result'].get('optionList', [])
                matching_options = [opt for opt in options if opt['fin_prdt_cd'] == base_item['fin_prdt_cd']]
                
                if matching_options:
                    for opt in matching_options:
                        product_data = {
                            'product_code': base_item['fin_prdt_cd'],
                            'type': 'deposit',
                            'name': base_item['fin_prdt_nm'],
                            'company': base_item['kor_co_nm'],
                            'interest_rate': float(opt.get('intr_rate', 0) or 0),
                            'special_rate': float(opt.get('intr_rate2', 0) or 0),
                            'term': int(opt.get('save_trm', 0) or 0),
                            'target': base_item.get('join_member', '')
                        }
                        
                        # DB에 저장 또는 업데이트
                        product, created = Product.objects.update_or_create(
                            product_code=product_data['product_code'],
                            type=product_data['type'],
                            defaults=product_data
                        )
                        
                        # 찜하기 상태 확인
                        is_liked = False
                        if user.is_authenticated:
                            is_liked = Favorite.objects.filter(
                                user=user,
                                type='deposit',
                                identifier=product.product_code
                            ).exists()
                        
                        response_data = {
                            **product_data,
                            'is_liked': is_liked
                        }
                        products.append(response_data)
        
        # 적금 데이터 변환 및 저장
        if 'result' in saving_data and 'baseList' in saving_data['result']:
            for base_item in saving_data['result']['baseList']:
                options = saving_data['result'].get('optionList', [])
                matching_options = [opt for opt in options if opt['fin_prdt_cd'] == base_item['fin_prdt_cd']]
                
                if matching_options:
                    for opt in matching_options:
                        product_data = {
                            'product_code': base_item['fin_prdt_cd'],
                            'type': 'saving',
                            'name': base_item['fin_prdt_nm'],
                            'company': base_item['kor_co_nm'],
                            'interest_rate': float(opt.get('intr_rate', 0) or 0),
                            'special_rate': float(opt.get('intr_rate2', 0) or 0),
                            'term': int(opt.get('save_trm', 0) or 0),
                            'target': base_item.get('join_member', '')
                        }
                        
                        # DB에 저장 또는 업데이트
                        product, created = Product.objects.update_or_create(
                            product_code=product_data['product_code'],
                            type=product_data['type'],
                            defaults=product_data
                        )
                        
                        # 찜하기 상태 확인
                        is_liked = False
                        if user.is_authenticated:
                            is_liked = Favorite.objects.filter(
                                user=user,
                                type='saving',
                                identifier=product.product_code
                            ).exists()
                        
                        response_data = {
                            **product_data,
                            'is_liked': is_liked
                        }
                        products.append(response_data)
        
        return Response(products)
    
    except Exception as e:
        print(f"Error in savings_list: {str(e)}")
        return Response(
            {"error": f"Failed to fetch financial products: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
'''
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
    serializer = GoodsSerializer(products, many=True)
    return Response(serializer.data)

'''

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favorite(request, identifier):
    """
    상품 찜하기 상태 확인 API
    identifier 형식: {type}_{company}_{name}
    """
    try:
        user = request.user
        logger.info(f"[check_favorite] User {user.id} checking favorite status for {identifier}")

        # identifier 파싱
        parts = identifier.split('_')
        if len(parts) < 3:
            return Response(
                {'error': '잘못된 식별자 형식입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        product_type = parts[0]
        company = parts[1]
        name = '_'.join(parts[2:])  # 상품명에 '_'가 포함될 수 있음

        # 상품 타입 검증
        if product_type not in ['deposit', 'saving']:
            return Response(
                {'error': '유효하지 않은 상품 유형입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 찜하기 상태 확인
        is_liked = Favorite.objects.filter(
            user=user,
            type=product_type,
            identifier=identifier
        ).exists()

        logger.info(f"[check_favorite] Product is {'liked' if is_liked else 'not liked'} by user {user.id}")
        return Response({
            'is_liked': is_liked
        })

    except Exception as e:
        logger.error(f"[check_favorite] Error: {str(e)}")
        return Response(
            {'error': '찜하기 상태 확인 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def stock_favorite(request, stock_code):
    """
    주식 찜하기/취소 API
    """
    try:
        # 작은따옴표 제거
        stock_code = stock_code.replace("'", "")
        
        # GET 요청: 찜하기 상태 확인
        if request.method == 'GET':
            is_liked = Favorite.objects.filter(
                user=request.user,
                type='stock',
                identifier=stock_code
            ).exists()
            count = Favorite.objects.filter(
                type='stock',
                identifier=stock_code
            ).count()
            return Response({
                'is_liked': is_liked,
                'count': count
            })

        # POST 요청: 찜하기
        elif request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                type='stock',
                identifier=stock_code
            )
            count = Favorite.objects.filter(
                type='stock',
                identifier=stock_code
            ).count()
            return Response({
                'message': '찜하기가 완료되었습니다.',
                'count': count
            })

        # DELETE 요청: 찜하기 취소
        elif request.method == 'DELETE':
            Favorite.objects.filter(
                user=request.user,
                type='stock',
                identifier=stock_code
            ).delete()
            count = Favorite.objects.filter(
                type='stock',
                identifier=stock_code
            ).count()
            return Response({
                'message': '찜하기가 취소되었습니다.',
                'count': count
            })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def goods_list(request):

    try:
        # 금/은 시세 API 호출
        headers = {
            'x-access-token': os.getenv("GOLD_API_KEY"),
            'Content-Type': 'application/json'
        }

        gold_res = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
        silver_res = requests.get('https://www.goldapi.io/api/XAG/USD', headers=headers)

        if gold_res.status_code != 200 or silver_res.status_code != 200:
            return Response({'error': '현물 시세 조회에 실패했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        gold_data = gold_res.json()
        silver_data = silver_res.json()

        # 응답 데이터 구성
        result = [
            {
                'id': 1,
                'name': '금 (Gold)',
                'company': 'GoldAPI.io',
                'current_price': gold_data.get('price'),
                'price_change': gold_data.get('ch'),
                'trade_volume': gold_data.get('vol'),
                'trade_value': gold_data.get('price_gram_24k'),
                'market_cap': None,
                'unit': 'USD per troy ounce',
                'type': 'goods'
            },
            {
                'id': 2,
                'name': '은 (Silver)',
                'company': 'GoldAPI.io',
                'current_price': silver_data.get('price'),
                'price_change': silver_data.get('ch'),
                'trade_volume': silver_data.get('vol'),
                'trade_value': silver_data.get('price_gram_24k'),
                'market_cap': None,
                'unit': 'USD per troy ounce',
                'type': 'goods'
            }
        ]

        return Response(result)

    except Exception as e:
        print(f"Error fetching goods data: {str(e)}")
        return Response(
            {'error': '현물 데이터를 불러오는데 실패했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def etf_favorite(request, etf_code):
    """
    ETF 찜하기/찜해제 토글 API
    """
    try:
        user = request.user
        print(f"[etf_favorite] User {user.id} accessing ETF {etf_code}")

        if request.method == 'GET':
            # 찜하기 상태 확인
            is_liked = Favorite.objects.filter(
                user=user,
                type='etf',
                identifier=etf_code
            ).exists()
            print(f"[etf_favorite] ETF {etf_code} is_liked: {is_liked}")
            return Response({
                'is_liked': is_liked
            })

        elif request.method == 'POST':
            # 찜하기 생성
            favorite, created = Favorite.objects.get_or_create(
                user=user,
                type='etf',
                identifier=etf_code
            )
            print(f"[etf_favorite] ETF {etf_code} favorite created: {created}")
            return Response({
                'message': '찜하기가 완료되었습니다.',
                'is_liked': True
            })

        elif request.method == 'DELETE':
            # 찜하기 삭제
            result = Favorite.objects.filter(
                user=user,
                type='etf',
                identifier=etf_code
            ).delete()
            
            if result[0] > 0:
                print(f"[etf_favorite] ETF {etf_code} favorite removed")
                return Response({
                    'message': '찜하기가 해제되었습니다.',
                    'is_liked': False
                })
            else:
                print(f"[etf_favorite] ETF {etf_code} favorite not found")
                return Response(
                    {'error': '찜하기가 존재하지 않습니다.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

    except Exception as e:
        print(f"[etf_favorite] Error: {str(e)}")
        return Response(
            {'error': '찜하기 처리 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def goods_favorite(request, goods_id):
    """
    현물 찜하기/찜해제 API
    """
    try:
        user = request.user
        print(f"[goods_favorite] User {user.id} accessing goods {goods_id}")

        if request.method == 'GET':
            # 찜하기 상태 확인
            is_liked = Favorite.objects.filter(
                user=user,
                type='goods',
                identifier=str(goods_id)
            ).exists()
            print(f"[goods_favorite] Goods {goods_id} is_liked: {is_liked}")
            return Response({
                'is_liked': is_liked
            })

        elif request.method == 'POST':
            # 찜하기 생성
            favorite, created = Favorite.objects.get_or_create(
                user=user,
                type='goods',
                identifier=str(goods_id)
            )
            print(f"[goods_favorite] Goods {goods_id} favorite created: {created}")
            return Response({
                'message': '찜하기가 완료되었습니다.',
                'is_liked': True
            })

        elif request.method == 'DELETE':
            # 찜하기 삭제
            result = Favorite.objects.filter(
                user=user,
                type='goods',
                identifier=str(goods_id)
            ).delete()
            
            if result[0] > 0:
                print(f"[goods_favorite] Goods {goods_id} favorite removed")
                return Response({
                    'message': '찜하기가 해제되었습니다.',
                    'is_liked': False
                })
            else:
                print(f"[goods_favorite] Goods {goods_id} favorite not found")
                return Response(
                    {'error': '찜하기가 존재하지 않습니다.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

    except Exception as e:
        print(f"[goods_favorite] Error: {str(e)}")
        return Response(
            {'error': '찜하기 처리 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )