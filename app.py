import streamlit as st
from core.collector import fetch_all_news
from core.crawler import fetch_gamejob
from core.ai import generate_daily_report
from core.storage import save_report_to_github, list_archived_reports, read_report
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="GameFeed AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.title("🎮 GameFeed AI")
    menu = st.radio("Navigation", ["🔥 게임 뉴스", "💼 채용 정보 (QA)", "🎨 채용 정보 (기획)", "📂 아카이브", "⚙️ 관리자"])
    
    st.markdown("---")
    st.caption("Data Sources: Inven, GameShot, Google, GameDonga, GameJob")

# --- Main Content ---
if menu == "🔥 게임 뉴스":
    st.header("🔥 최신 게임 뉴스 브리핑")
    
    # 검색바
    search_query = st.text_input("뉴스 검색", placeholder="키워드를 입력하세요...")
    
    news_list = fetch_all_news()
    
    # 필터링
    if search_query:
        news_list = [n for n in news_list if search_query.lower() in n['title'].lower()]
    
    # 카드 UI (3열)
    cols = st.columns(3)
    for i, news in enumerate(news_list):
        with cols[i % 3]:
            with st.container(border=True):
                # st.image(news['image'], use_column_width=True) # 이미지 품질 이슈로 일단 제외하거나 플레이스홀더 사용
                st.subheader(news['title'])
                st.caption(f"{news['source']} | {news['date']}")
                st.write(news['summary'])
                st.markdown(f"[기사 원문 보기]({news['link']})")

elif menu == "💼 채용 정보 (QA)":
    st.header("🐛 QA / 테스팅 채용 정보")
    jobs = fetch_gamejob(24) # QA Code
    
    if jobs:
        for job in jobs:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.subheader(job['title'])
                c1.write(f"🏢 **{job['company']}** | {job['career']}")
                c2.write(f"📅 {job['date']}")
                c2.markdown(f"[공고 확인]({job['link']})")
    else:
        st.warning("채용 정보를 불러오지 못했습니다.")

elif menu == "🎨 채용 정보 (기획)":
    st.header("📝 게임 기획 / 디자인 채용 정보")
    jobs = fetch_gamejob(9) # Design Code
    
    if jobs:
        for job in jobs:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.subheader(job['title'])
                c1.write(f"🏢 **{job['company']}** | {job['career']}")
                c2.write(f"📅 {job['date']}")
                c2.markdown(f"[공고 확인]({job['link']})")
    else:
        st.warning("채용 정보를 불러오지 못했습니다.")

elif menu == "📂 아카이브":
    st.header("📚 AI 뉴스 요약 아카이브")
    
    report_files = list_archived_reports()
    
    if report_files:
        selected_report = st.selectbox("리포트 선택", report_files)
        if selected_report:
            with st.spinner("리포트 불러오는 중..."):
                content = read_report(selected_report)
                st.markdown("---")
                st.markdown(content)
    else:
        st.info("저장된 리포트가 없습니다. 관리자 메뉴에서 생성해주세요.")

elif menu == "⚙️ 관리자":
    st.header("⚙️ 관리자 대시보드")
    password = st.text_input("비밀번호", type="password")
    if password == "0421": # 임시 비번
        st.success("로그인 성공")
        
        # 1. 뉴스 현황
        news = fetch_all_news()
        st.metric("현재 수집된 뉴스", f"{len(news)} 건")
        
        # 2. 아카이빙 버튼
        st.subheader("🤖 일일 리포트 생성 & 저장")
        if st.button("🚀 뉴스 요약 및 아카이빙 실행"):
            with st.spinner("Gemini가 뉴스를 분석 중입니다..."):
                report_content = generate_daily_report(news)
                st.markdown("### 미리보기")
                st.markdown(report_content)
                
            with st.spinner("GitHub에 저장 중..."):
                success, msg = save_report_to_github(report_content)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
    else:
        if password:
            st.error("비밀번호가 틀렸습니다.")
