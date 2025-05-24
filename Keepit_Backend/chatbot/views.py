from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .utils import get_chatbot_response

# Create your views here.

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_chat_session(request):
    """새로운 채팅을 시작합니다."""
    category = request.data.get('category')
    if category not in ['page_help', 'product_info']:
        return Response({
            'error': '유효하지 않은 카테고리입니다. (page_help 또는 product_info)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 이전 세션이 있다면 삭제
    ChatSession.objects.filter(user=request.user).delete()
    
    session = ChatSession.objects.create(
        user=request.user,
        category=category
    )
    
    # 초기 환영 메시지 생성
    if category == 'page_help':
        welcome_message = "안녕하세요! Keepit 웹사이트 도우미입니다. 웹사이트 사용에 대해 어떤 것이 궁금하신가요?"
    else:
        welcome_message = "안녕하세요! 금융 상품 전문가입니다. 어떤 금융 상품이나 투자에 대해 알고 싶으신가요?"
    
    ChatMessage.objects.create(
        session=session,
        is_user=False,
        content=welcome_message
    )
    
    return Response({
        'session_id': session.id,
        'welcome_message': welcome_message
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message(request, session_id):
    """채팅 메시지를 주고받습니다."""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({
            'error': '채팅 세션을 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    message = request.data.get('message')
    if not message:
        return Response({
            'error': '메시지 내용이 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 사용자 메시지 저장
    ChatMessage.objects.create(
        session=session,
        is_user=True,
        content=message
    )
    
    # 이전 대화 내역 가져오기 (최근 5개 메시지)
    chat_history = ChatMessage.objects.filter(session=session).order_by('-created_at')[:5][::-1]
    
    # AI 응답 생성
    ai_response = get_chatbot_response(session.category, message, chat_history)
    
    # AI 응답 저장
    ChatMessage.objects.create(
        session=session,
        is_user=False,
        content=ai_response
    )
    
    return Response({
        'response': ai_response
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_chat_sessions(request):
    """사용자의 채팅 세션 목록을 반환합니다."""
    sessions = ChatSession.objects.filter(user=request.user)
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_chat_session(request, session_id):
    """특정 채팅 세션의 상세 정보를 반환합니다."""
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({
            'error': '채팅 세션을 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChatSessionSerializer(session)
    return Response(serializer.data)
