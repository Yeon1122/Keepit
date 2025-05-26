from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import TestResult
from .serializers import TestResultSerializer
import os
import joblib
import pandas as pd

# Create your views here.

# 모델 로드
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'recommendations', 'data', 'models', 'recommendation_model.pkl')
model = joblib.load(MODEL_PATH)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_test_page(request):
    """투자 성향 테스트 문항을 반환합니다."""
    test_questions = {
        'questions': [
            {
                'id': 'age',
                'question': '나이를 입력해주세요',
                'type': 'number',
                'placeholder': '나이를 입력해주세요'
            },
            {
                'id': 'gender',
                'question': '성별을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': 'M', 'text': '남성'},
                    {'value': 'F', 'text': '여성'}
                ]
            },
            {
                'id': 'income',
                'question': '연간 소득(만원)을 입력해주세요',
                'type': 'number',
                'placeholder': '예: 5000'
            },
            {
                'id': 'assets',
                'question': '총 자산(만원)을 입력해주세요',
                'type': 'number',
                'placeholder': '예: 10000'
            },
            {
                'id': 'risk_tolerance',
                'question': '위험 성향을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': 'low', 'text': '안정 추구형'},
                    {'value': 'medium', 'text': '위험 중립형'},
                    {'value': 'high', 'text': '위험 선호형'}
                ]
            },
            {
                'id': 'financial_knowledge',
                'question': '금융 지식 수준을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': '낮음', 'text': '낮음'},
                    {'value': '보통', 'text': '보통'},
                    {'value': '높음', 'text': '높음'}
                ]
            },
            {
                'id': 'investment_experience',
                'question': '투자 경험을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': '없음', 'text': '투자 경험 없음'},
                    {'value': '1~3년', 'text': '1~3년'},
                    {'value': '3년 이상', 'text': '3년 이상'}
                ]
            },
            {
                'id': 'saving_goal',
                'question': '저축/투자 목표를 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': '단기 여행', 'text': '단기 여행'},
                    {'value': '결혼 준비', 'text': '결혼 준비'},
                    {'value': '내 집 마련', 'text': '내 집 마련'},
                    {'value': '은퇴 준비', 'text': '은퇴 준비'},
                    {'value': '목돈 마련', 'text': '목돈 마련'}
                ]
            },
            {
                'id': 'preferred_term',
                'question': '선호하는 투자 기간을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': '단기', 'text': '1년 미만'},
                    {'value': '중기', 'text': '1~3년'},
                    {'value': '장기', 'text': '3년 이상'}
                ]
            },
            {
                'id': 'user_type',
                'question': '직업군을 선택해주세요',
                'type': 'select',
                'choices': [
                    {'value': '사회초년생', 'text': '사회초년생'},
                    {'value': '직장인', 'text': '직장인'},
                    {'value': '주부', 'text': '주부'},
                    {'value': '은퇴자', 'text': '은퇴자'}
                ]
            }
        ]
    }
    return Response(test_questions)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_test(request):
    """테스트 결과를 제출하고 저장합니다."""
    required_fields = [
        'age', 'gender', 'income', 'assets', 'risk_tolerance',
        'financial_knowledge', 'investment_experience', 'saving_goal',
        'preferred_term', 'user_type'
    ]
    
    # 필수 필드 검증
    for field in required_fields:
        if field not in request.data:
            return Response({
                'error': f'{field} 필드가 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # XGBoost 모델을 위한 입력 데이터 준비
    input_data = pd.DataFrame([{
        'age': request.data['age'],
        'gender': request.data['gender'],
        'income': request.data['income'],
        'assets': request.data['assets'],
        'risk_tolerance': request.data['risk_tolerance'],
        'financial_knowledge': request.data['financial_knowledge'],
        'investment_experience': request.data['investment_experience'],
        'saving_goal': request.data['saving_goal'],
        'preferred_term': request.data['preferred_term'],
        'user_type': request.data['user_type']
    }])
    
    # 모델 예측
    predictions = model.predict(input_data)
    
    # 예측 결과에 따른 risk_type 결정
    # predictions는 [deposit, saving, stock, etf, goods] 형태의 이진 값
    if predictions[0][0] == 1:  # deposit이 추천된 경우
        risk_type = 'conservative'
    elif predictions[0][2] == 1:  # stock이 추천된 경우
        risk_type = 'aggressive'
    else:
        risk_type = 'moderate'
    
    # 이전 결과 삭제
    TestResult.objects.filter(user=request.user).delete()
    
    # 결과 저장
    result = TestResult.objects.create(
        user=request.user,
        risk_type=risk_type,
        test_data=request.data,  # JSON 형태로 전체 테스트 데이터 저장
    )
    
    # 응답 데이터 준비
    response_data = {
        'risk_type': risk_type,
        'test_data': request.data,
        'recommendations': {
            'deposit': bool(predictions[0][0]),
            'saving': bool(predictions[0][1]),
            'stock': bool(predictions[0][2]),
            'etf': bool(predictions[0][3]),
            'goods': bool(predictions[0][4])
        }
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_test_result(request):
    """사용자의 최신 테스트 결과를 반환합니다."""
    try:
        result = TestResult.objects.filter(user=request.user).latest('created_at')
        
        # 모델 재예측
        input_data = pd.DataFrame([result.test_data])
        predictions = model.predict(input_data)
        
        response_data = {
            'risk_type': result.risk_type,
            'test_data': result.test_data,
            'recommendations': {
                'deposit': bool(predictions[0][0]),
                'saving': bool(predictions[0][1]),
                'stock': bool(predictions[0][2]),
                'etf': bool(predictions[0][3]),
                'goods': bool(predictions[0][4])
            }
        }
        
        return Response(response_data)
    except TestResult.DoesNotExist:
        return Response(None, status=200)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_test_result(request):
    """테스트 결과를 삭제합니다."""
    TestResult.objects.filter(user=request.user).delete()
    return Response({
        'message': '테스트 결과가 삭제되었습니다.'
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_test_result(request, userid):
    """특정 사용자의 최신 테스트 결과를 반환합니다."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        target_user = User.objects.get(userid=userid)
        
        result = TestResult.objects.filter(user=target_user).latest('created_at')
        
        # 위험 성향에 따른 타입과 설명
        risk_type_info = {
            'conservative': {
                'type': '안정형 투자자',
                'description': '안정적인 수익을 추구하며 원금 보존을 중요시합니다.',
                'recommendation': '예금, 적금, 채권 등 안정적인 상품 위주의 투자를 추천합니다.'
            },
            'moderate': {
                'type': '중립형 투자자',
                'description': '적절한 위험을 감수하며 중위험-중수익을 추구합니다.',
                'recommendation': '채권형 펀드와 주식형 펀드를 혼합한 투자를 추천합니다.'
            },
            'aggressive': {
                'type': '공격형 투자자',
                'description': '높은 수익을 위해 적극적인 투자를 선호합니다.',
                'recommendation': '주식, 해외투자 등 높은 수익을 노릴 수 있는 투자를 추천합니다.'
            }
        }

        response_data = {
            'risk_type': result.risk_type,
            'description': risk_type_info[result.risk_type],
            'recommendations': result.recommendations if hasattr(result, 'recommendations') else {}
        }
        
        return Response(response_data)
    except User.DoesNotExist:
        return Response({
            'error': '존재하지 않는 사용자입니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    except TestResult.DoesNotExist:
        return Response(None, status=200)
        # return Response({
        #     'error': '테스트 결과가 없습니다.'
        # }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=500)