# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserUpdateSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # JWT 토큰으로부터 인증된 사용자
        return Response({
            "userid": user.userid,
            "nickname": user.nickname,
            "email": user.email,
            "name": user.name,
            "birth_year": user.birth_year if user.birth_year else None,
            "birth_month": user.birth_month if user.birth_month else None,
            "birth_day": user.birth_day if user.birth_day else None,
            "region_city": user.region_city.name if user.region_city else None,
            "region_district": user.region_district.name if user.region_district else None,
        })
    
class MyPagePutView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
# userid 중복확인
class CheckUserIdView(APIView):
    def get(self, request):
        userid = request.query_params.get("value")
        if not userid:
            return Response({"error": "값이 필요합니다."}, status=400)

        exists = User.objects.filter(userid=userid).exists()
        return Response({"is_available": not exists})

# nickname 중복확인
class CheckNicknameView(APIView):
    def get(self, request):
        nickname = request.query_params.get("value")
        if not nickname:
            return Response({"error": "값이 필요합니다."}, status=400)

        exists = User.objects.filter(nickname=nickname).exists()
        return Response({"is_available": not exists})