from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import json

BASE_URL = "https://library.sogang.ac.kr/"


# 하위 페이지 크롤링 함수
def crawl_page(url, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    # 이미 방문한 URL은 스킵
    if url in visited_urls:
        return {"url": url, "description": "Already visited", "content": []}
    visited_urls.add(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Section 추출 (하위 페이지 섹션)
    title = soup.find("h2", id="divTitle").get_text(strip=True) if soup.find("h2", id="divTitle") else "No Title"

    # Breadcrumb에서 대분류와 중분류 추출
    breadcrumbs = soup.select("#divLocation ul li a")
    category = breadcrumbs[1].get_text(strip=True) if len(breadcrumbs) > 1 else "No Category"
    subcategory = breadcrumbs[2].get_text(strip=True) if len(breadcrumbs) > 2 else "No Subcategory"

    # Description 및 테이블 및 리스트 데이터 처리
    description = []
    for section_tag in soup.select(".guide h3.titleStyle1"):
        section_title = section_tag.get_text(strip=True)
        section_content = []

        # 테이블 처리
        table = section_tag.find_next("table")
        if table:
            table_data = {
                "caption": table.caption.get_text(strip=True) if table.caption else None,
                "columns": [th.get_text(strip=True) for th in table.select("thead th")],
                "rows": [
                    [td.get_text(strip=True) for td in row.select("td")]
                    for row in table.select("tbody tr")
                ],
            }
            section_content.append(table_data)

        # listStyle5 및 listStyle6 처리
        for list_item in section_tag.find_all_next(["li", "p"], class_=["listStyle5", "listStyle6"]):
            section_content.append(list_item.get_text(strip=True))

        description.append({"section": section_title, "content": section_content})

    return {
        "category": category,
        "subcategory": subcategory,
        "url": url,
        "title": title,
        "description": description,
    }


# 메뉴 구조 크롤링 함수
def crawl_menu(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    menu_data = []

    for menu_item in soup.select("#divTopMenu ul li a"):
        href = menu_item["href"]
        full_url = urljoin(base_url, href)

        try:
            page_data = crawl_page(full_url)
            menu_data.append(page_data)
        except Exception as e:
            print(f"Failed to crawl {full_url}: {e}")

    return menu_data


# 크롤링 시작
def main():
    print("크롤링 시작...")
    menu_data = crawl_menu(BASE_URL, BASE_URL)

    save_directory = "database/raw"
    os.makedirs(save_directory, exist_ok=True)

    with open(os.path.join(save_directory, "sogang_library_structured.json"), "w", encoding="utf-8") as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=4)

    print(f"크롤링 완료! {len(menu_data)}개의 메뉴를 수집했고, 데이터는 {save_directory}/sogang_library_structured.json에 저장되었습니다.")


if __name__ == "__main__":
    main()
