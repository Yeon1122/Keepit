import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FSS_API_KEY")

API_URLS = {
    'deposit': 'https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json',
    'saving': 'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json',
    # 주식/ETF 등은 추가로 구현
}

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


def fetch_stock_by_code(stock_code):
    # 예시: 실제 주식 API 연결 필요
    # 응답 JSON을 받아서 파싱하고 반환
    return {
        'stock_code': stock_code,
        'current_price': 123456,
        'price_change': 1.23,
        'company': '샘플기업',
    }