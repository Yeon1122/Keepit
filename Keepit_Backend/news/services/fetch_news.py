import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()  # .env 파일 로드

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def clean_text(text):
    # HTML 태그 제거
    text = re.sub(r"<.*?>", "", text)
    # 특수문자 제거 (단, 한글, 영문, 숫자, 일부 문장부호는 유지)
    text = re.sub(r"[^\w\s\.,\-()]", "", text)
    return text.strip()

def is_stock_related(title, company_name):
    """주식 관련 뉴스인지 확인"""
    # 회사명이 정확히 포함되어 있는지 확인
    if company_name not in title:
        return False
    
    # 주식/투자 관련 키워드 - 더 일반적인 키워드 포함
    stock_keywords = [
        '주가', '주식', '증시', '실적', '매출', '영업이익', '순이익',
        '투자', '공시', '상장', '거래', '시장', '코스피', '코스닥',
        '전망', '목표가', '매수', '매도', '신고가', '신저가',
        '증권', '금융', '상승', '하락', '급등', '급락', '호실적',
        '실적발표', '기업', '성장', 'CEO', '대표', '사업', '계획'
    ]
    
    # 회사명이 제목에 있고, 주식 관련 키워드가 없는 경우에도
    # 일부 뉴스는 포함시키기 위해 키워드 매칭 기준 완화
    if any(keyword in title for keyword in ['대표', '사장', '부회장', '회장', '임원', '경영', '사업', '계획']):
        return True
        
    return any(keyword in title for keyword in stock_keywords)

def remove_similar_news(news_list, threshold=0.85):
    if not news_list:
        return []
    
    # 제목에서 회사명, 날짜, 기자명 등 제거하고 핵심 내용만 비교
    def clean_title_for_comparison(title):
        # 대괄호로 둘러싸인 내용 제거 (예: [특징주], [시그널] 등)
        title = re.sub(r'\[[^\]]*\]', '', title)
        # 날짜 패턴 제거
        title = re.sub(r'\d{4}[-\.년]\s*\d{1,2}[-\.월]\s*\d{1,2}[일]?', '', title)
        # 기자명 패턴 제거
        title = re.sub(r'\w+\s*(기자|특파원|팀장|연구원)', '', title)
        # 언론사 이름 제거
        title = re.sub(r'\/[\w\s]+', '', title)
        # 모든 공백 문자를 단일 공백으로 변경하고 양쪽 공백 제거
        title = ' '.join(title.split())
        return title.strip()

    # 정확히 같은 제목 체크를 위한 집합
    seen_titles = set()
    unique_news = []

    for news in news_list:
        clean_title = clean_title_for_comparison(news["title"])
        if clean_title not in seen_titles:
            seen_titles.add(clean_title)
            unique_news.append(news)

    # 유사도 검사로 한번 더 필터링
    if len(unique_news) > 1:
        texts = [clean_title_for_comparison(news["title"]) for news in unique_news]
        tfidf = TfidfVectorizer().fit_transform(texts)
        sim_matrix = cosine_similarity(tfidf)
        
        final_news = []
        seen_indices = set()
        
        for i in range(len(unique_news)):
            if i in seen_indices:
                continue
                
            final_news.append(unique_news[i])
            seen_indices.add(i)
            
            for j in range(i + 1, len(unique_news)):
                if j not in seen_indices and sim_matrix[i][j] > threshold:
                    seen_indices.add(j)
        
        return final_news
    
    return unique_news

def fetch_unique_stock_news(stock_name, max_results=5):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        print("Error: Naver API credentials not found")
        return []

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    
    search_query = stock_name
    params = {
        "query": search_query,
        "display": 100,
        "sort": "date",
    }

    try:
        print(f"Fetching news for: {search_query}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        print(f"Found {len(items)} items")

        # 뉴스 제목과 내용 정리
        for item in items:
            item["title"] = clean_text(item["title"])
            item["description"] = clean_text(item["description"])
            # 언론사 추출 (link에서 추출)
            try:
                news_source = item["link"].split("://")[1].split("/")[0]
                if "news.naver.com" in item["link"]:
                    # 네이버 뉴스인 경우 원본 언론사 추출
                    news_source = item["link"].split("sid=")[1][:3]
                    news_sources = {
                        "001": "연합뉴스",
                        "003": "뉴시스",
                        "008": "머니투데이",
                        "009": "매일경제",
                        "011": "서울경제",
                        "014": "파이낸셜뉴스",
                        "015": "한국경제",
                        "016": "헤럴드경제",
                        "018": "이데일리",
                        "021": "문화일보",
                        "022": "세계일보",
                        "029": "디지털타임스",
                        "032": "경향신문",
                        "081": "서울신문",
                        "277": "아시아경제",
                        "421": "뉴스1",
                    }
                    news_source = news_sources.get(news_source, news_source)
                # 도메인에서 언론사 이름 정제
                news_source = news_source.replace("www.", "").split(".")[0]
            except:
                news_source = "언론사"
            
            # 언론사 정보를 별도 필드로 저장
            item["news_source"] = news_source

        # 제목에 회사명이 있는 뉴스와 없는 뉴스를 분리
        title_matched_items = []
        other_items = []
        
        for item in items:
            if stock_name in item["title"]:
                title_matched_items.append(item)
            elif any(keyword in item["title"] for keyword in [
                '주가', '주식', '증시', '실적', '매출', '영업이익', '순이익',
                '투자', '공시', '상장', '거래', '시장', '코스피', '코스닥',
                '전망', '목표가', '매수', '매도', '신고가', '신저가',
                '증권', '금융', '상승', '하락', '급등', '급락', '호실적',
                '실적발표', '기업', '성장', 'CEO', '대표', '사업', '계획',
                '체결', '계약', '협약', '특허', '기술', '개발'
            ]):
                other_items.append(item)

        print(f"Title matched items: {len(title_matched_items)}")
        print(f"Other related items: {len(other_items)}")

        # 각각 중복 제거 (유사도 기준 강화)
        unique_title_matched = remove_similar_news(title_matched_items, threshold=0.75)
        unique_others = remove_similar_news(other_items, threshold=0.75)

        # 제목 매칭된 뉴스를 우선으로 하고, 부족하면 나머지 뉴스로 채움
        final_items = unique_title_matched
        remaining_slots = max_results - len(final_items)
        
        if remaining_slots > 0:
            final_items.extend(unique_others[:remaining_slots])

        return [
            {
                "title": item["title"],
                "description": item["description"],
                "link": item["link"],
                "pubDate": item["pubDate"],
                "news_source": item["news_source"]  # 언론사 정보를 별도 필드로 전달
            }
            for item in final_items[:max_results]
        ]
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return [] 

