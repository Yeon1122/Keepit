from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockNews
from .serializers import StockNewsSerializer
from news.services.fetch_news import fetch_unique_stock_news
from datetime import datetime
from dateutil import parser as date_parser 

import os
from dotenv import load_dotenv
load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

@api_view(['GET'])
def get_stock_news(request, stock_code):
    news_qs = StockNews.objects.filter(stock_code=stock_code).order_by('-published_at')

    if not news_qs.exists():
        news_data = fetch_unique_stock_news(stock_code)

        news_objects = []
        for item in news_data:
            published = date_parser.parse(item['pubDate'])  # 문자열 → datetime 객체 변환

            news = StockNews(
                stock_code=stock_code,
                title=item['title'],
                summary=item['description'],
                link=item['link'],
                published_at=published,  # ✔ 여기가 중요!
            )
            news_objects.append(news)

        StockNews.objects.bulk_create(news_objects)
        news_qs = StockNews.objects.filter(stock_code=stock_code).order_by('-published_at')

    serializer = StockNewsSerializer(news_qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
