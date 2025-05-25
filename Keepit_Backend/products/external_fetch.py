import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FSS_API_KEY")
KIS_APP_KEY = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET = os.getenv("KIS_APP_SECRET")

API_URLS = {
    'deposit': 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json',
    'saving': 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json',
}
KIS_BASE_URL = "https://openapi.koreainvestment.com:9443"

# 전역 캐시
access_token = None
token_expire_time = 0  # 초 단위

# 예금 적금 정보 불러오기
def fetch_products(product_type):
    url = API_URLS[product_type]
    res = requests.get(url, params={'auth': API_KEY, 'topFinGrpNo': '020000', 'pageNo': 1})
    base_list = res.json().get('result', {}).get('baseList', [])
    option_list = res.json().get('result', {}).get('optionList', [])

    option_map = {(o['fin_co_no'], o['fin_prdt_cd']): o for o in option_list}

    result = []
    for item in base_list:
        key = (item['fin_co_no'], item['fin_prdt_cd'])
        opt = option_map.get(key)
        result.append({
            'name': item.get('fin_prdt_nm'),
            'company': item.get('kor_co_nm'),
            'link': item.get('join_link', ''),
            'interest_rate': opt.get('intr_rate') if opt else None,
            'special_rate': opt.get('intr_rate2') if opt else None,
            'term': opt.get('save_trm') if opt else None,
            'target': item.get('join_member'),
        })
    return result

# 한국투자증권 API 인증
def get_access_token():
    global access_token, token_expire_time
    
    now = time.time()
    
    # 유효한 토큰이 있다면 재사용
    if access_token and now < token_expire_time:
        return access_token

    # 새로 발급
    url = f"{KIS_BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    data = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET
    }

    try:
        res = requests.post(url, json=data, headers=headers)
        res.raise_for_status()  # HTTP 에러 체크
        res_data = res.json()

        access_token = res_data.get("access_token")
        expires_in = int(res_data.get("expires_in", 0))  # 보통 초 단위
        token_expire_time = now + expires_in - 60  # 1분 여유

        return access_token
    except Exception as e:
        print(f"토큰 발급 중 오류 발생: {e}")
        return None

# 주식 정보 불러오기
def fetch_stock_by_code(stock_code):
    # 작은따옴표 제거
    stock_code = stock_code.replace("'", "")
    
    token = get_access_token()
    if not token:
        return None

    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
        "tr_id": "FHKST01010100",  # 시세 조회용 TR ID
    }
    params = {
        "fid_cond_mrkt_div_code": "J",  # J: 코스피 / Q: 코스닥
        "fid_input_iscd": stock_code,
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()  # HTTP 에러 체크
        output = res.json().get("output", {})
        
        # 문자열 값을 숫자로 변환하는 함수
        def safe_convert(value, convert_type=float):
            try:
                return convert_type(value) if value is not None else 0
            except (ValueError, TypeError):
                return 0
                
        return {
            'id': None,
            'type': 'stock',
            'name': output.get('hts_kor_isnm'),
            'link': None,
            'stock_code': stock_code,
            'current_price': safe_convert(output.get('stck_prpr')),
            'price_change': safe_convert(output.get('prdy_vrss')),
            'market_cap': safe_convert(output.get('hts_avls')),
            'trade_volume': safe_convert(output.get('acml_vol')),
            'trade_value': safe_convert(output.get('acml_tr_pbmn')),
        }
    except Exception as e:
        print(f"주식 정보 조회 중 오류 발생: {e}")
        return None

# 주식 상세정보 불러오기
def fetch_stock_detail_by_code(stock_code):
    token = get_access_token()
    if not token:
        return None

    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
        "tr_id": "FHKST01010100",
    }
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()  # HTTP 에러 체크
        output = res.json().get("output", {})
        
        return {
            'id': None,
            'type': 'stock',
            'name': output.get('hts_kor_isnm'),
            'link': None,
            'stock_code': stock_code,
            'market_type': output.get('mksc_shrn_iscd'),
            'current_price': output.get('stck_prpr'),
            'price_change': output.get('prdy_vrss'),
            'sector': output.get('bstp_kor_isnm'),
            'warning_info': output.get('stck_rsk_yn'),
            'open_price': output.get('stck_oprc'),
            'high_price': output.get('stck_hgpr'),
            'low_price': output.get('stck_lwpr'),
            'base_price': output.get('stck_sdpr'),
            'weighted_avg_price': output.get('wghn_avrg_stck_prc'),
            'high_52w': output.get('h52w_prc'),
            'high_52w_date': output.get('h52w_prc_dt'),
            'low_52w': output.get('l52w_prc'),
            'low_52w_date': output.get('l52w_prc_dt'),
            'per': output.get('per'),
            'pbr': output.get('pbr'),
            'eps': output.get('eps'),
            'bps': output.get('bps'),
            'market_cap': output.get('hts_avls'),
            'listed_shares': output.get('lstn_stcn'),
            'settlement_month': output.get('stac_month'),
            'per_value': output.get('per'),
            'trade_volume': output.get('acml_vol'),
            'trade_value': output.get('acml_tr_pbmn'),
            'foreign_ownership': output.get('frgn_hldn_qty'),
            'short_selling_allowed': output.get('short_over_yn'),
            'short_selling_volume': output.get('short_over_prc'),
        }
    except Exception as e:
        print(f"주식 상세 정보 조회 중 오류 발생: {e}")
        return None

# ETF 정보 불러오기
def fetch_etf_by_code(etf_code):
    token = get_access_token()
    if not token:
        return None

    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET,
        "tr_id": "FHKST01010100",
    }
    params = {
        "fid_cond_mrkt_div_code": "J",  # 대부분 ETF는 코스피
        "fid_input_iscd": etf_code,
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()  # HTTP 에러 체크
        output = res.json().get("output", {})
        
        def safe_convert(value, convert_type=float):
            try:
                return convert_type(value) if value is not None else 0
            except (ValueError, TypeError):
                return 0

        return {
            'type': 'etf',
            "etf_code": etf_code,
            "name": output.get("hts_kor_isnm"),
            "current_price": safe_convert(output.get("stck_prpr")),
            "price_change": safe_convert(output.get("prdy_vrss")),
            "market_cap": safe_convert(output.get("hts_avls")),
            "trade_volume": safe_convert(output.get("acml_vol")),
            "trade_value": safe_convert(output.get("acml_tr_pbmn")),
        }
    except Exception as e:
        print(f"ETF 정보 조회 중 오류 발생: {e}")
        return None

# 예금 적금 찜한 상품 비교
def fetch_product_details_by_name(product_names, product_type):
    """
    상품 이름 리스트와 상품 타입(deposit/saving)을 받아,
    해당 이름의 상품 상세정보를 외부 API로부터 가져온다.
    """
    API_URL = (
        'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        if product_type == "deposit"
        else "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    )

    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }

    res = requests.get(API_URL, params=params)
    data = res.json()

    base_list = data.get('result', {}).get('baseList', [])
    option_list = data.get('result', {}).get('optionList', [])

    # 상품 이름으로 필터링
    matched_products = []
    for base in base_list:
        if base['fin_prdt_nm'] in product_names:
            # 해당 상품의 옵션 찾기
            product_options = [
                opt for opt in option_list
                if opt['fin_co_no'] == base['fin_co_no'] and opt['fin_prdt_cd'] == base['fin_prdt_cd']
            ]
            
            # 각 옵션에 대해 상품 정보 생성
            for opt in product_options:
                matched_products.append({
                    'name': base['fin_prdt_nm'],
                    'company': base['kor_co_nm'],
                    'interest_rate': float(opt['intr_rate'] or 0),
                    'special_rate': float(opt['intr_rate2'] or 0),
                    'term': int(opt['save_trm'] or 0)
                })

    return matched_products