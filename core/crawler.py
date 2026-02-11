import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import streamlit as st

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def parse_company(onclick_text: str) -> str:
    if not onclick_text:
        return ""
    parts = re.findall(r"'([^']*)'", onclick_text)
    return parts[4] if len(parts) >= 5 else ""

@st.cache_data(ttl=3600)  # 1시간 캐싱
def fetch_gamejob(duty_code: int, pages: int = 1):
    """
    게임잡 채용정보 크롤링
    duty_code: 24(QA), 9(게임기획)
    """
    base_url = f"https://www.gamejob.co.kr/Recruit/joblist?menucode=duty&duty={duty_code}"
    jobs = []
    
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        # 1페이지만 긁어옴 (속도 최적화)
        resp = session.get(base_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser") # lxml 대신 html.parser 사용 (호환성)
        
        for tit in soup.select("div.tit"):
            a_tag = tit.select_one("a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            company = parse_company(a_tag.get("onclick", ""))
            link = urljoin(base_url, a_tag.get("href", ""))
            
            # 메타 정보 (경력, 학력 등)
            meta_info = [s.get_text(strip=True) for s in tit.select("p.info > span")]
            career = meta_info[0] if meta_info else ""
            
            # 마감일/등록일
            date_span = tit.find_parent("tr").select_one("span.date") if tit.find_parent("tr") else None
            date_text = date_span.get_text(strip=True) if date_span else ""

            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "career": career,
                "date": date_text
            })
            
    except Exception as e:
        print(f"GameJob Crawl Error: {e}")
        return []

    return jobs
