# users/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User, Follow
from .serializers import UserCreateSerializer, UserUpdateSerializer, UserLoginSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(APIView):
    def post(self, request):
        print("🪵 로그인 요청 데이터:", request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'userid': user.userid,
                "is_authenticated": True,
                "nickname": user.nickname,
                "email": user.email,
                "name": user.name,
                "birth_year": user.birth_year if user.birth_year else None,
                "birth_month": user.birth_month if user.birth_month else None,
                "birth_day": user.birth_day if user.birth_day else None,
                "region_city": user.region_city.name if user.region_city else None,
                "region_district": user.region_district.name if user.region_district else None,
                })
        return Response({
            'is_authenticated': False,
            'errors': serializer.errors,
            'received_data': request.data 
            }, status=400)

# 마이페이지 조회
class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "user_id": user.id,
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
    
    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user_id": user.id,
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
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        request.user.delete()
        return Response({"message": "회원 탈퇴 완료"}, status=204)

# 다른 유저 프로필 조회
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "해당 유저가 존재하지 않습니다."}, status=404)

        is_following = Follow.objects.filter(from_user=request.user, to_user=target_user).exists()

        follower_count = Follow.objects.filter(to_user=target_user).count()
        following_count = Follow.objects.filter(from_user=target_user).count()
        # post_count = Post.objects.filter(user=target_user).count()

        # favorites = Favorite.objects.filter(user=target_user).select_related('product')
        # favorite_products = [
        #     {
        #         "product_id": fav.product.id,
        #         "category": fav.product.category if hasattr(fav.product, 'category') else None
        #         "name": fav.product.name,
        #     }
        #     for fav in favorites
        # ]

        return Response({
            "user_id": target_user.id,
            "nickname": target_user.nickname,
            "is_following": is_following,

            # "follower_count": follower_count,
            # "following_count": following_count,
            # "post_count": post_count,
            # "favorite_products": favorite_products
        }) 
    
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

# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"detail": "로그아웃 완료"}, status=204)
        except Token.DoesNotExist:
            return Response({"detail": "이미 로그아웃 상태입니다."}, status=400)
        

# follow
class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    # 팔로우
    def post(self, request, user_id):
        from_user = request.user
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "message": "존재하지 않는 사용자입니다.",
                "status": 404,
                "data": None
            }, status=404)

        if from_user == to_user:
            return Response({
                "message": "자기 자신은 팔로우할 수 없습니다.",
                "status": 400,
                "data": None
            }, status=400)

        follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({
                "message": "이미 팔로우한 사용자입니다.",
                "status": 400,
                "data": None
            }, status=400)

        return Response({
            "message": "해당 유저를 팔로우했습니다.",
            "status": 200,
            "data": {
                "follower_id": from_user.id,
                "following_id": to_user.id
            }
        }, status=200)
    
    # 언팔로우
    def delete(self, request, user_id):
        from_user = request.user
        try:
            follow = Follow.objects.get(from_user=from_user, to_user_id=user_id)
            follow.delete()
            return Response({
                "message": "팔로우를 취소했습니다.",
                "status": 200,
                "data": {
                    "follower_id": from_user.id,
                    "following_id": int(user_id)
                }
            })
        except Follow.DoesNotExist:
            return Response({
                "message": "팔로우하지 않은 사용자입니다.",
                "status": 400,
                "data": None
            }, status=400)




class FollowListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        following_data = [
            {
                "user_id": follow.to_user.id,
                "nickname": follow.to_user.nickname
            }
            for follow in user.following.select_related('to_user')
        ]

        follower_data = [
            {
                "user_id": follow.from_user.id,
                "nickname": follow.from_user.nickname
            }
            for follow in user.followers.select_related('from_user')
        ]

        return Response({
            "message": "팔로우 정보를 불러왔습니다.",
            "status": 200,
            "data": {
                "following": following_data,
                "followers": follower_data
            }
        })
