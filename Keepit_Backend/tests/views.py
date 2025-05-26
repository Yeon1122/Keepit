from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import TestResult
from .serializers import TestResultSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_test_page(request):
    """투자 성향 테스트 문항을 반환합니다."""
    test_questions = {
        'questions': [
            {
                'id': 1,
                'question': '당신의 나이는?',
                'choices': [
                    {'value': 1, 'text': '20대 이하'},
                    {'value': 2, 'text': '30~40대'},
                    {'value': 3, 'text': '50대 이상'}
                ]
            },
            {
                'id': 2,
                'question': '당신의 투자 경험은 어느 정도인가요?',
                'choices': [
                    {'value': 1, 'text': '없음'},
                    {'value': 2, 'text': '약간 있음'},
                    {'value': 3, 'text': '매우 많음'}
                ]
            },
            {
                'id': 3,
                'question': '투자 손실이 발생했을 때 당신의 반응은?',
                'choices': [
                    {'value': 1, 'text': '전부 인출'},
                    {'value': 2, 'text': '일부 유지'},
                    {'value': 3, 'text': '추가 매수'}
                ]
            },
            {
                'id': 4,
                'question': '당신의 주 수입원은?',
                'choices': [
                    {'value': 1, 'text': '불안정 (자영업, 아르바이트 등)'},
                    {'value': 2, 'text': '보통 (정규직 등)'},
                    {'value': 3, 'text': '매우 안정 (공무원, 연금 등)'}
                ]
            },
            {
                'id': 5,
                'question': '투자 시 기대 수익률은?',
                'choices': [
                    {'value': 1, 'text': '3% 이하'},
                    {'value': 2, 'text': '5~8%'},
                    {'value': 3, 'text': '10% 이상'}
                ]
            },
            {
                'id': 6,
                'question': '갑작스러운 큰 지출이 생기면 어떻게 대응할 수 있나요?',
                'choices': [
                    {'value': 1, 'text': '전혀 대비 안 됨'},
                    {'value': 2, 'text': '일부 대비됨'},
                    {'value': 3, 'text': '충분히 대비됨'}
                ]
            }
        ]
    }
    return Response(test_questions)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_test(request):
    """테스트 결과를 제출하고 저장합니다."""
    # 각 문항의 응답 검증
    required_fields = ['q1_age', 'q2_experience', 'q3_loss_response', 
                      'q4_income', 'q5_expected_return', 'q6_emergency']
    
    for field in required_fields:
        value = request.data.get(field)
        if not value or not isinstance(value, int) or value < 1 or value > 3:
            return Response({
                'error': f'{field} 문항에 대한 올바른 응답이 필요합니다. (1-3 사이의 정수)'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # 총점 계산
    total_score = sum(request.data.get(field) for field in required_fields)
    
    # 투자 성향 결정
    if total_score <= 9:
        risk_type = 'conservative'
    elif total_score <= 13:
        risk_type = 'moderate'
    else:
        risk_type = 'aggressive'
    
    # 이전 결과 삭제
    TestResult.objects.filter(user=request.user).delete()
    
    # 결과 저장
    result = TestResult.objects.create(
        user=request.user,
        total_score=total_score,
        risk_type=risk_type,
        q1_age=request.data['q1_age'],
        q2_experience=request.data['q2_experience'],
        q3_loss_response=request.data['q3_loss_response'],
        q4_income=request.data['q4_income'],
        q5_expected_return=request.data['q5_expected_return'],
        q6_emergency=request.data['q6_emergency']
    )
    
    serializer = TestResultSerializer(result)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_test_result(request):
    """사용자의 최신 테스트 결과를 반환합니다."""
    try:
        result = TestResult.objects.filter(user=request.user).latest('created_at')
        
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
            'type': risk_type_info[result.risk_type]['type'],
            'total_score': result.total_score,
            'description': risk_type_info[result.risk_type],
            'q1_age': result.q1_age,
            'q2_experience': result.q2_experience,
            'q3_loss_response': result.q3_loss_response,
            'q4_income': result.q4_income,
            'q5_expected_return': result.q5_expected_return,
            'q6_emergency': result.q6_emergency,
        }
        
        return Response(response_data)
    except TestResult.DoesNotExist:
        return Response(None, status=200)
        # return Response({
        #     'error': '테스트 결과가 없습니다.'
        # }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_test_result(request):
    """이전 테스트 결과를 삭제하고 다시 테스트할 수 있게 합니다."""
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
            'type': risk_type_info[result.risk_type]['type'],
            'total_score': result.total_score,
            'description': risk_type_info[result.risk_type],
            'q1_age': result.q1_age,
            'q2_experience': result.q2_experience,
            'q3_loss_response': result.q3_loss_response,
            'q4_income': result.q4_income,
            'q5_expected_return': result.q5_expected_return,
            'q6_emergency': result.q6_emergency,
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
