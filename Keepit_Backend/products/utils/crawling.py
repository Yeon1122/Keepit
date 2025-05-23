import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def crawl_top_200_stocks():
    data = []

    for page in range(1, 5):  # 1~4페이지 = 총 200개 종목
        url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page={page}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        rows = soup.select("table.type_2 tr")

        for row in rows:
            link = row.select_one("td a.tltle")
            if link:
                name = link.text.strip()
                code = link['href'].split('code=')[-1]
                code = f"'{code.zfill(6)}'"
                data.append({'종목명': name, '종목코드': code})

    df = pd.DataFrame(data)
    return df

# df.to_csv('./products/utils/naver_top200_stocks.csv', index=False, encoding='utf-8-sig')
# print("CSV 저장 완료!")


url = "https://finance.naver.com/api/sise/etfItemList.nhn?etfType=0&targetColumn=market_sum&sortOrder=desc"
response = requests.get(url)
etf_json = response.json()
etfItemList = etf_json["result"]['etfItemList']
df = pd.DataFrame(etfItemList)[["itemcode", "itemname"]]
df.columns = ["종목코드", "종목명"]  # 컬럼명 한글로 바꾸기

# CSV 저장
df.to_csv("etf_code_name.csv", index=False, encoding="utf-8-sig")