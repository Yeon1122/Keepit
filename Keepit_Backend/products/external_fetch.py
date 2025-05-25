import os
import requests
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("FSS_API_KEY")
KIS_APP_KEY = os.getenv("KIS_APP_KEY")
KIS_APP_SECRET = os.getenv("KIS_APP_SECRET")
access_token = None

API_URLS = {
    'deposit': 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json',
    'saving': 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json',
}
KIS_BASE_URL = "https://openapi.koreainvestment.com:9443"

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
    global access_token
    if access_token:
        return access_token

    url = f"{KIS_BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    data = {
        "grant_type": "client_credentials",
        "appkey": KIS_APP_KEY,
        "appsecret": KIS_APP_SECRET
    }
    res = requests.post(url, json=data, headers=headers)
    access_token = res.json().get("access_token")
    return access_token

# 주식 정보 불러오기
def fetch_stock_by_code(stock_code):
    # 작은따옴표 제거
    stock_code = stock_code.replace("'", "")
    
    token = get_access_token()
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
    res = requests.get(url, headers=headers, params=params)
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

# 주식 상세정보 불러오기
def fetch_stock_detail_by_code(stock_code):
    token = get_access_token()
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
    res = requests.get(url, headers=headers, params=params)
    output = res.json().get("output", {})
    return {
        'id': None,
        'type': 'stock',
        'name': output.get('hts_kor_isnm'),
        # 'company': None,
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

# ETF 정보 불러오기
def fetch_etf_by_code(etf_code):
    token = get_access_token()
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

    res = requests.get(url, headers=headers, params=params)
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


# 예금 적금 찜한 상품 비교
def fetch_product_details_by_name(product_names, product_type):
    """
    상품 이름 리스트와 상품 타입(deposit/saving)을 받아,
    해당 이름의 상품 상세정보를 외부 API로부터 가져온다.
    """

    API_URLS = (
        'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        if product_type == "deposit"
        else "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    )

    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",   # 은행
        "pageNo": 1
    }

    response = requests.get(API_URLS, params=params)
    if response.status_code != 200:
        return []

    result = response.json().get("result", {})
    base_list = result.get("baseList", [])
    option_list = result.get("optionList", [])

    product_meta = {
        p["fin_prdt_cd"]: {
            "name": p.get("fin_prdt_nm", "").strip(),
            "company": p.get("kor_co_nm", "").strip(),
            "target": p.get("join_member", "").strip()
        }
        for p in base_list
    }

    matched_products = []
    for p in option_list:
        code = p.get("fin_prdt_cd")
        meta = product_meta.get(code)
        if not meta:
            continue

        name = meta["name"]
        for keyword in product_names:
            if keyword in name or name in keyword:
                matched_products.append({
                    "name": name,
                    "company": meta["company"],
                    "target": meta["target"],
                    "interest_rate": float(p.get("intr_rate", 0)),
                    "special_rate": float(p.get("intr_rate2", 0)),
                    "term": int(p.get("save_trm", 12)),
                })
                break
    
    # print(f"✅ 매칭된 상품 수: {len(matched_products)}")
    # for m in matched_products:
    #     print(f" - {m['name']} (이율: {m['interest_rate']}%, 기간: {m['term']}개월)")


    return matched_products