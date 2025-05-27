import os
import requests
import time
from dotenv import load_dotenv
from .utils.stock_code_loader import load_stock_name_map

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

    # 주식 코드로 실제 회사명 가져오기
    stock_name_map = load_stock_name_map()
    company_name = stock_name_map.get(stock_code)

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
        
        # 매핑된 이름이 없으면 API 응답의 hts_kor_isnm 사용
        if not company_name:
            company_name = output.get('hts_kor_isnm', '')
        if not company_name:
            company_name = f"{stock_code} 주식"
        
        # 업종명은 bstp_kor_isnm에서 가져오되, '/' 구분자가 있으면 마지막 부분을 사용
        sector = output.get('bstp_kor_isnm', '')
        if '/' in sector:
            sector = sector.split('/')[-1].strip()

        def safe_convert(value, convert_type=float):
            try:
                return convert_type(value) if value is not None else None
            except (ValueError, TypeError):
                return None

        # 가격 변동 방향 표시 (▲, ▼)와 변동가를 함께 표시
        price_change = safe_convert(output.get('prdy_vrss'))
        price_change_str = ''
        if price_change:
            direction = '▲' if price_change > 0 else '▼' if price_change < 0 else ''
            # 변동가가 있을 때만 방향과 함께 표시하고 '원' 단위 추가
            if direction:
                price_change_str = f"{direction} {abs(price_change):,.0f}원"
            else:
                price_change_str = f"{price_change:,.0f}원"

        # 날짜 형식 변환 (YYYYMMDD -> YYYY년 MM월 DD일)
        def format_date(date_str):
            if not date_str or len(date_str) != 8:
                return None
            try:
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}년 {month}월 {day}일"
            except:
                return None

        high_52w_date = format_date(output.get('w52_hgpr_date'))
        low_52w_date = format_date(output.get('w52_lwpr_date'))
        
        return {
            'id': None,
            'type': 'stock',
            'name': company_name,
            'link': None,
            'stock_code': stock_code,
            'market_type': output.get('rprs_mrkt_kor_name'),
            'current_price': safe_convert(output.get('stck_prpr')),  # 현재가
            'price_change': price_change,  # 전일 대비 (숫자)
            'price_change_str': price_change_str,  # 전일 대비 (방향 포함, 예: "▲ 1,000")
            'sector': sector,
            'warning_info': output.get('stck_rsk_yn'),
            'open_price': safe_convert(output.get('stck_oprc')),  # 시가
            'high_price': safe_convert(output.get('stck_hgpr')),  # 고가
            'low_price': safe_convert(output.get('stck_lwpr')),  # 저가
            'base_price': safe_convert(output.get('stck_sdpr')),  # 기준가
            'weighted_avg_price': safe_convert(output.get('wghn_avrg_stck_prc')),  # 가중평균
            'high_52w': safe_convert(output.get('w52_hgpr')),  # 52주 최고
            'high_52w_date': high_52w_date,  # 52주 최고일 (YYYY년 MM월 DD일)
            'low_52w': safe_convert(output.get('w52_lwpr')),  # 52주 최저
            'low_52w_date': low_52w_date,  # 52주 최저일 (YYYY년 MM월 DD일)
            'per': safe_convert(output.get('per')),  # PER
            'pbr': safe_convert(output.get('pbr')),  # PBR
            'eps': safe_convert(output.get('eps')),  # EPS
            'bps': safe_convert(output.get('bps')),  # BPS
            'market_cap': safe_convert(output.get('hts_avls')),  # 시가총액
            'listed_shares': safe_convert(output.get('lstn_stcn')),  # 상장주식수
            'settlement_month': output.get('stac_month'),  # 결산월
            'trade_volume': safe_convert(output.get('acml_vol')),  # 거래량
            'trade_value': safe_convert(output.get('acml_tr_pbmn')),  # 거래대금
            'foreign_ownership': safe_convert(output.get('frgn_hldn_qty')),  # 외국인보유량
            'short_selling_allowed': output.get('short_over_yn'),  # 공매도가능여부
            'short_selling_volume': safe_convert(output.get('short_over_prc')),  # 공매도수량
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

    try:
        res = requests.get(API_URL, params=params)
        res.raise_for_status()  # HTTP 에러 체크
        data = res.json()

        base_list = data.get('result', {}).get('baseList', [])
        option_list = data.get('result', {}).get('optionList', [])

        if not base_list or not option_list:
            print(f"API 응답에 데이터가 없습니다: {data}")
            return []

        # 상품 이름으로 필터링
        matched_products = []
        for base in base_list:
            if base['fin_prdt_nm'] in product_names:
                # 해당 상품의 옵션 찾기
                product_options = [
                    opt for opt in option_list
                    if opt['fin_co_no'] == base['fin_co_no'] and 
                    opt['fin_prdt_cd'] == base['fin_prdt_cd']
                ]
                
                if product_options:  # 옵션이 있는 경우만 처리
                    # 각 옵션에 대해 상품 정보 생성
                    for opt in product_options:
                        try:
                            # save_trm이 없거나 0인 경우 기본값 12 사용
                            term = opt.get('save_trm')
                            if not term or term == '0':
                                term = '12'
                                
                            matched_products.append({
                                'name': base['fin_prdt_nm'],
                                'company': base['kor_co_nm'],
                                'interest_rate': float(opt.get('intr_rate', 0) or 0),
                                'special_rate': float(opt.get('intr_rate2', 0) or 0),
                                'term': int(term)
                            })
                        except (ValueError, TypeError) as e:
                            print(f"상품 데이터 변환 중 오류: {e}, 상품: {base['fin_prdt_nm']}, 옵션: {opt}")
                            continue

        if not matched_products:
            print(f"매칭된 상품이 없습니다. 검색한 상품명: {product_names}")
            # 매칭된 상품이 없을 경우 기본 데이터 추가
            for name in product_names:
                matched_products.append({
                    'name': name,
                    'company': '정보 없음',
                    'interest_rate': 0,
                    'special_rate': 0,
                    'term': 12
                })

        return matched_products

    except requests.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return []