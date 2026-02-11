import feedparser
import streamlit as st
import datetime

FEEDS = [
    {"name": "게임동아", "url": "https://game.donga.com/feeds/rss/"},
    {"name": "게임샷", "url": "https://rss.gameshot.net/gameshot/article_xml.php"},
    {"name": "구글 뉴스 (게임)", "url": "https://news.google.com/rss/search?q=game&hl=ko&gl=KR&ceid=KR:ko"},
    {"name": "인벤", "url": "http://webzine.inven.co.kr/news/rss.php"}
]

@st.cache_data(ttl=600) # 10분 캐싱
def fetch_all_news():
    all_news = []
    for feed in FEEDS:
        try:
            d = feedparser.parse(feed['url'])
            for entry in d.entries[:5]: # 피드당 최신 5개
                # 이미지 추출 시도 (media_content or summary img)
                image_url = "https://via.placeholder.com/150?text=No+Image"
                if 'media_content' in entry and entry.media_content:
                    image_url = entry.media_content[0]['url']
                
                published = entry.get('published', datetime.datetime.now().strftime("%Y-%m-%d"))
                
                all_news.append({
                    "source": feed['name'],
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get('summary', '')[:100] + "...",
                    "image": image_url,
                    "date": published
                })
        except Exception as e:
            print(f"RSS Error ({feed['name']}): {e}")
            
    return all_news
