from openai import OpenAI
from django.conf import settings

def get_chatbot_response(category, message, chat_history=None):
    """OpenAI API를 사용하여 챗봇 응답을 생성합니다."""
    
    # OpenAI API 키가 없는 경우 기본 응답 제공
    if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
        if category == 'page_help':
            return "안녕하세요! Keepit 웹사이트 도우미입니다. 현재 OpenAI API가 설정되지 않아 기본 응답을 제공하고 있습니다. 웹사이트 사용에 대해 궁금한 점이 있으시면 언제든 문의해주세요!"
        else:  # product_info
            return "안녕하세요! 금융 상품 전문가입니다. 현재 OpenAI API가 설정되지 않아 기본 응답을 제공하고 있습니다. 예금, 적금, 주식, ETF 등 다양한 금융 상품에 대해 궁금한 점이 있으시면 언제든 문의해주세요!"
    
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # 시스템 메시지 설정
    if category == 'page_help':
        system_message = """당신은 Keepit 웹사이트의 도우미입니다. 
        사용자들의 웹사이트 사용과 관련된 질문에 친절하게 답변해주세요.
        Keepit은 투자 성향 테스트, 커뮤니티, 자산 관리 기능을 제공하는 웹사이트입니다."""
    else:  # product_info
        system_message = """당신은 금융 상품 전문가입니다.
        사용자들의 금융 상품과 투자에 관한 질문에 전문적으로 답변해주세요.
        투자의 위험성도 함께 설명해주세요."""
    
    # 대화 히스토리 구성
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    if chat_history:
        for msg in chat_history:
            role = "user" if msg.is_user else "assistant"
            messages.append({"role": role, "content": msg.content})
    
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"죄송합니다. 응답을 생성하는 중에 오류가 발생했습니다: {str(e)}" 