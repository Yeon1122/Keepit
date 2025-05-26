from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockNews
from .serializers import StockNewsSerializer
from .services.fetch_news import fetch_unique_stock_news
from products.external_fetch import fetch_stock_detail_by_code

@api_view(['GET'])
def get_stock_news(request, stock_code):
    try:
        print(f"\n=== Starting news fetch for stock code: {stock_code} ===")
        
        # 주식 정보를 가져와서 회사명 얻기
        stock_info = fetch_stock_detail_by_code(stock_code)
        print(f"Stock info received: {stock_info}")
        
        if not stock_info:
            print("No stock info found")
            return Response([], status=status.HTTP_200_OK)
            
        # hts_kor_isnm을 사용하여 회사명 가져오기
        company_name = stock_info.get('name')  # 'name' 필드로 변경
        if not company_name:
            company_name = stock_info.get('hts_kor_isnm')  # 백업으로 hts_kor_isnm 사용
            
        if not company_name:
            print("No company name found")
            return Response([], status=status.HTTP_200_OK)
            
        print(f"Searching news for company: {company_name}")
        # 회사명으로 뉴스 검색
        news_items = fetch_unique_stock_news(company_name)
        print(f"Found {len(news_items)} news items")
        
        # 프론트엔드 NewsCard 컴포넌트의 props와 일치하도록 데이터 구조 변경
        formatted_news = [{
            'title': item['title'],
            'url': item['link'],
            'date': item['pubDate']
        } for item in news_items]
        
        print(f"Returning {len(formatted_news)} formatted news items")
        print("=== News fetch completed ===\n")
        return Response(formatted_news, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error in get_stock_news: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response([], status=status.HTTP_200_OK)  # 에러가 나도 빈 배열 반환


