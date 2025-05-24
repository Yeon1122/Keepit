import openai
from django.conf import settings

def get_chatbot_response(category, message, chat_history=None):
    """OpenAI API를 사용하여 챗봇 응답을 생성합니다."""
    openai.api_key = settings.OPENAI_API_KEY
    
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"죄송합니다. 응답을 생성하는 중에 오류가 발생했습니다: {str(e)}" 