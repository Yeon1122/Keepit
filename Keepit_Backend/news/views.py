from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockNews
from .serializers import StockNewsSerializer

@api_view(['GET'])
def get_stock_news(request, stock_code):
    news_qs = StockNews.objects.filter(stock_code=stock_code).order_by('-published_at')
    serializer = StockNewsSerializer(news_qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

