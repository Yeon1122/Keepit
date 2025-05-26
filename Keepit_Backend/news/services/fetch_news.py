import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def clean_text(text):
    return re.sub(r'<.*?>', '', text).strip()

def remove_similar_news(news_list, threshold=0.85):
    texts = [news['description'] for news in news_list]
    tfidf = TfidfVectorizer().fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf)
    seen = set()
    unique_news = []

    for i in range(len(news_list)):
        if i in seen:
            continue
        unique_news.append(news_list[i])
        for j in range(i + 1, len(news_list)):
            if sim_matrix[i][j] > threshold:
                seen.add(j)
    return unique_news

def fetch_unique_stock_news(stock_name, max_results=5):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": stock_name,
        "display": 20,
        "sort": "date",
    }

    response = requests.get(url, headers=headers, params=params)
    items = response.json().get("items", [])

    for item in items:
        item["description"] = clean_text(item["description"])
        item["title"] = clean_text(item["title"])

    filtered_items = remove_similar_news(items)

    return [
        {
            "title": item["title"],
            "description": item["description"],
            "link": item["link"],
            "pubDate": item["pubDate"],
        }
        for item in filtered_items[:max_results]
    ]
