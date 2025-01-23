import requests
from bs4 import BeautifulSoup
import json
import re

def clean_filename(filename):
    """
    파일 이름에서 Windows에서 허용되지 않는 문자를 제거
    """
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def extract_submenu_links(base_url):
    """
    소페이지에서 세부 메뉴 URL 추출-세부메뉴 버튼있는경우에
    """
    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 세부 메뉴 URL이 포함된 <a> 태그를 선택
        submenu_links = soup.select('a')  # 필요한 경우 정확한 CSS 선택자 수정

        extracted_links = []
        for link in submenu_links:
            href = link.get('href')
            if href and href.startswith('/'):  # 상대 URL인 경우 처리
                href = f"https://library.sogang.ac.kr{href}"
            if href and "htmlmanager" in href:  # 특정 URL 조건 필터링
                extracted_links.append(href)
        return list(set(extracted_links))  # 중복 제거
    except Exception as e:
        print(f"에러 발생: {base_url} - {e}")
        return []

def crawl_page_content(url):
    """
    주어진 URL에서 콘텐츠 크롤링
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 기본적으로 div#divContents 안의 내용을 가져옴
        content = soup.select_one('div#divContents')

        if content:
            return content.get_text(strip=True)
        else:
            return "내용이 없습니다."
    except Exception as e:
        print(f"에러 발생: {url} - {e}")
        return "크롤링 실패"

def save_to_json(data, file_name):
    """
    데이터를 JSON 파일로 저장
    """
    file_name = clean_filename(file_name)  # 파일 이름 정리
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 대분류, 중분류, 소분류 구조 정의 (URL은 빈 문자열로 초기화)
url_data = [
    {
        "대분류": "도서관 소개",
        "중분류": "알림/문의",
        "소분류": [
            {"이름": "FAQ 1p", "URL": "https://library.sogang.ac.kr/faqlib/faq?code=all"},
            {"이름": "FAQ 2p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=2&code=all"},
            {"이름": "FAQ 3p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=3&code=all"},
            {"이름": "FAQ 4p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=4&code=all"},
            {"이름": "FAQ 5p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=5&code=all"},
            {"이름": "FAQ 6p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=6&code=all"},
            {"이름": "FAQ 7p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=7&code=all"},
            {"이름": "FAQ 8p", "URL": "https://library.sogang.ac.kr/faqlib/faq?pn=8&code=all"},
        ]
    }
]

def main():
    """
    전체 크롤링 실행
    """
    for section in url_data:
        대분류 = section["대분류"]
        중분류 = section["중분류"]

        for 소분류 in section["소분류"]:
            소분류_이름 = 소분류["이름"]
            소분류_URL = 소분류["URL"]

            print(f"크롤링 중: 대분류={대분류}, 중분류={중분류}, 소분류={소분류_이름}, URL={소분류_URL}")

            # 소분류 페이지 크롤링
            content = crawl_page_content(소분류_URL)

            # JSON 파일로 저장
            file_name = f"{대분류}_{중분류}_{소분류_이름}.json"
            save_to_json(
                {
                    "대분류": 대분류,
                    "중분류": 중분류,
                    "소분류": 소분류_이름,
                    "URL": 소분류_URL,
                    "내용": content
                },
                file_name
            )
            print(f"저장 완료: {file_name}")

        
if __name__ == "__main__":
    main()