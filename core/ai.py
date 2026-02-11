import google.generativeai as genai
import os
import streamlit as st

def generate_daily_report(news_list):
    """
    뉴스 리스트를 받아 Gemini로 마크다운 리포트 생성
    """
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "❌ API Key가 설정되지 않았습니다."

    genai.configure(api_key=api_key)
    # 최신 모델 사용
    model = genai.GenerativeModel('gemini-2.5-flash')

    # 프롬프트 구성
    prompt = """
    당신은 베테랑 게임 뉴스 에디터입니다. 
    아래 제공된 [오늘의 게임 뉴스]를 바탕으로, 게임 개발자와 게이머를 위한 '일일 브리핑'을 작성해주세요.

    [작성 규칙]
    1. **헤드라인**: 오늘의 가장 중요한 이슈 1개를 선정해 제목으로 쓰세요. (이모지 포함)
    2. **주요 뉴스 (Top 3)**: 트렌드, 대작 게임, 기업 이슈 위주로 3개를 뽑아 3줄 요약하세요.
    3. **단신**: 나머지 뉴스 중 흥미로운 것들을 글머리 기호로 나열하세요.
    4. **형식**: 가독성 좋은 Markdown 포맷으로 작성하세요.

    [오늘의 게임 뉴스 데이터]
    """
    
    for news in news_list[:15]: # 너무 많으면 토큰 낭비니 상위 15개만
        prompt += f"- {news['title']} ({news['source']})\n"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🤖 AI 에러 발생: {str(e)}"
