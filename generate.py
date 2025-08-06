import os
import datetime

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

# --- 1. 우리동네뉴스(최신 5건) 크롤링 ---
def fetch_region_news(city_no=None, dvsn_no=None):
    """
    우리동네뉴스(최신 5건)를 가져옵니다.
    city_no, dvsn_no를 지정하지 않으면 '종합' 목록을 반환합니다.
    """
    url     = "https://land.naver.com/news/region.naver"
    headers = {"User-Agent": "Mozilla/5.0"}
    params  = {}
    if city_no and dvsn_no:
        params["city_no"] = city_no
        params["dvsn_no"] = dvsn_no

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 종합(전체) 영역 또는 특정 지역 영역 선택
    container = (
        soup.select_one("#total_news ul.category_list")
        or soup.select_one("#region_news_area")
    )
    if not container:
        return []

    news_list = []
    for li in container.select("li")[:5]:
        # 두 번째 <a> (target="_blank") 가 실제 기사 링크
        links = li.select("a[target='_blank']")
        if not links:
            continue
        tag = links[-1]
        title = tag.get_text(strip=True)
        href  = tag["href"]
        if href.startswith("//"):
            href = "https:" + href
        news_list.append({"title": title, "link": href})

    return news_list


# --- 2. 시세 데이터 (더미 예시) ---
def get_price_data():
    return [
        {"name": "강남 푸르지오", "price": "19억 5,000만원"},
        {"name": "잠실 엘스",     "price": "17억 2,000만원"},
        {"name": "마포 래미안",   "price": "13억 8,000만원"},
    ]


# --- 3. Jinja2 템플릿 렌더링 ---
def render_template(news, prices):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    output = template.render(
        news=news,
        prices=prices,
        update_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    os.makedirs("output", exist_ok=True)
    with open('output/index.html', 'w', encoding='utf-8') as f:
        f.write(output)


# --- 4. 진입점 ---
def main():
    news   = fetch_region_news()      # 종합 우리동네뉴스 5건
    prices = get_price_data()
    render_template(news, prices)
    print("✅ index.html 생성 완료 → output 폴더 확인")


if __name__ == "__main__":
    main()
