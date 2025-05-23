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
    return {
        'id': None,
        'type': 'stock',
        'name': output.get('hts_kor_isnm'),
        'link': None,
        'stock_code': stock_code,
        'current_price': output.get('stck_prpr'),
        'price_change': output.get('prdy_vrss'),
        'market_cap': output.get('hts_avls'),
        'trade_volume': output.get('acml_vol'),
        'trade_value': output.get('acml_tr_pbmn'),
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

    return {
        'type': 'etf',
        "etf_code": etf_code,
        "name": output.get("hts_kor_isnm"),
        "current_price": output.get("stck_prpr"),
        "price_change": output.get("prdy_vrss"),
        "market_cap": output.get("hts_avls"),
        "trade_volume": output.get("acml_vol"),
        "trade_value": output.get("acml_tr_pbmn"),
        # "nav": output.get("nav"),  # 순자산가치
        # "nav_change": output.get("nav_chg_rt"),
    }