import pandas as pd
import os
from .crawling import crawl_top_200_stocks

def load_top_stock_codes():
    df = crawl_top_200_stocks()
    return df['종목코드'].tolist()
    # csv_path = os.path.join(os.path.dirname(__file__), 'naver_top200_stocks.csv')
    # df = pd.read_csv(csv_path, dtype=str)
    # return df['종목코드'].apply(lambda x: x.strip("'")).tolist()

def load_stock_name_map():
    df = crawl_top_200_stocks()
    return dict(zip(df['종목코드'], df['종목명']))
    # csv_path = os.path.join(os.path.dirname(__file__), 'naver_top200_stocks.csv')
    # df = pd.read_csv(csv_path, dtype=str)
    # df['종목코드'] = df['종목코드'].apply(lambda x: x.strip("'"))
    # return dict(zip(df['종목코드'], df['종목명']))


def load_top_etf_codes():
    df = pd.read_csv('products/data/etf_code_name.csv', encoding='utf-8-sig', dtype=str)
    print("[DEBUG] 컬럼명:", df.columns.tolist()) 
    return df['종목코드'].tolist()

def load_etf_name_map():
    df = pd.read_csv('products/data/etf_code_name.csv', encoding='utf-8-sig', dtype=str)
    return dict(zip(df['종목코드'], df['종목명']))