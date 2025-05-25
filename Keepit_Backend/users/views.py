# users/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User, Follow
from .serializers import UserCreateSerializer, UserUpdateSerializer, UserLoginSerializer
from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.contrib.auth import get_user_model
from community.models import Post
from django.db.models import Count
from products.models import Favorite, Product

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
                'user_id': user.id,
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
        
        # 게시글 통계
        posts = Post.objects.filter(author=user)
        total_posts = posts.count()
        
        # 게시판 별 게시글 수
        posts_by_type = posts.values('board_type').annotate(count=Count('id'))
        posts_count = {
            'free': 0,
            'question': 0
        }
        for item in posts_by_type:
            posts_count[item['board_type']] = item['count']
        
        # 최근 게시글 목록 (최대 5개)
        recent_posts = posts.select_related('author').prefetch_related('likes').order_by('-created_at')[:5]
        recent_posts_data = [{
            'id': post.id,
            'board_type': post.get_board_type_display(),  # 한글 표시 ('자유게시판' 또는 '질문게시판')
            'title': post.title,
            'likes_count': post.likes.count(),
            'created_at': post.created_at
        } for post in recent_posts]

        # 찜한 상품 목록 가져오기
        favorites = Favorite.objects.filter(user=user)
        liked_products = []
        
        for fav in favorites:
            if fav.type in ['deposit', 'saving']:
                try:
                    product_id = int(fav.identifier)
                    product = Product.objects.filter(id=product_id).first()
                    
                    if product:
                        liked_products.append({
                            'id': product.id,
                            'type': product.type,
                            'name': product.name,
                            'company': product.company,
                            'interest_rate': product.interest_rate,
                            'special_rate': product.special_rate,
                            'term': product.term,
                            'target': product.target,
                            'is_liked': True
                        })
                except (ValueError, Product.DoesNotExist):
                    continue

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
            "followers": list(user.followers.values_list('id', flat=True)),
            "following": list(user.following.values_list('id', flat=True)),
            # 게시글 정보 추가
            "posts_summary": {
                "total_posts": total_posts,
                "free_posts": posts_count['free'],
                "question_posts": posts_count['question']
            },
            "recent_posts": recent_posts_data,
            # 찜한 상품 목록 추가
            "liked_products": liked_products
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

    def get(self, request, userid):
        try:
            target_user = User.objects.get(userid=userid)
        except User.DoesNotExist:
            return Response({"message": "해당 유저가 존재하지 않습니다."}, status=404)

        is_following = Follow.objects.filter(from_user=request.user, to_user=target_user).exists()

        # followers / following
        followers = list(Follow.objects.filter(to_user=target_user).values("from_user__id", "from_user__nickname"))
        following = list(Follow.objects.filter(from_user=target_user).values("to_user__id", "to_user__nickname"))

        # 게시글 통계
        posts = Post.objects.filter(author=target_user)
        total_posts = posts.count()
        
        # 게시판 별 게시글 수
        posts_by_type = posts.values('board_type').annotate(count=Count('id'))
        posts_count = {
            'free': 0,
            'question': 0
        }
        for item in posts_by_type:
            posts_count[item['board_type']] = item['count']
        
        # 최근 게시글 목록 (최대 5개)
        recent_posts = posts.select_related('author').prefetch_related('likes').order_by('-created_at')[:5]
        recent_posts_data = [{
            'id': post.id,
            'board_type': post.get_board_type_display(),
            'title': post.title,
            'likes_count': post.likes.count(),
            'created_at': post.created_at
        } for post in recent_posts]

        return Response({
            "user_id": target_user.id,
            "userid": target_user.userid,
            "nickname": target_user.nickname,
            "email": target_user.email,
            "followers": followers,
            "following": following,
            "is_following": is_following,
            # 게시글 정보 추가
            "posts_summary": {
                "total_posts": total_posts,
                "free_posts": posts_count['free'],
                "question_posts": posts_count['question']
            },
            "recent_posts": recent_posts_data
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
        
#팔로우
class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        from_user = request.user
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "존재하지 않는 사용자입니다.", "status": 404}, status=404)

        if from_user == to_user:
            return Response({"message": "자기 자신은 팔로우할 수 없습니다.", "status": 400}, status=400)

        follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({"message": "이미 팔로우한 사용자입니다.", "status": 400}, status=400)

        return Response({
            "message": "해당 유저를 팔로우했습니다.",
            "status": 200,
            "data": {
                "is_following": True,
                "followers": list(to_user.followers.values_list('id', flat=True)),
                "following": list(to_user.following.values_list('id', flat=True)),
            }
        })

    def delete(self, request, user_id):
        from_user = request.user
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "존재하지 않는 사용자입니다.", "status": 404}, status=404)

        try:
            follow = Follow.objects.get(from_user=from_user, to_user=to_user)
            follow.delete()

            return Response({
                "message": "팔로우를 취소했습니다.",
                "status": 200,
                "data": {
                    "is_following": False,
                    "followers": list(to_user.followers.values_list('id', flat=True)),
                    "following": list(to_user.following.values_list('id', flat=True)),
                }
            })
        except Follow.DoesNotExist:
            return Response({"message": "팔로우하지 않은 사용자입니다.", "status": 400}, status=400)




# class FollowListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         following_data = [
#             {
#                 "user_id": follow.to_user.id,
#                 "nickname": follow.to_user.nickname,
#                 "userid": follow.to_user.userid
#             }
#             for follow in user.following.select_related('to_user')
#         ]

#         follower_data = [
#             {
#                 "user_id": follow.from_user.id,
#                 "nickname": follow.from_user.nickname,
#                 "userid": follow.to_user.userid
#             }
#             for follow in user.followers.select_related('from_user')
#         ]

#         return Response({
#             "message": "팔로우 정보를 불러왔습니다.",
#             "status": 200,
#             "data": {
#                 "following": following_data,
#                 "followers": follower_data
#             }
#         })
    

class FollowListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userid):  # ✅ 여기!
        target_user = get_object_or_404(User, userid=userid)

        following_data = [
            {
                "user_id": follow.to_user.id,
                "nickname": follow.to_user.nickname,
                "userid": follow.to_user.userid
            }
            for follow in target_user.following.select_related('to_user')
        ]

        follower_data = [
            {
                "user_id": follow.from_user.id,
                "nickname": follow.from_user.nickname,
                "userid": follow.from_user.userid
            }
            for follow in target_user.followers.select_related('from_user')
        ]

        return Response({
            "message": f"{target_user.nickname}의 팔로우 정보를 불러왔습니다.",
            "status": 200,
            "data": {
                "following": following_data,
                "followers": follower_data
            }
        })