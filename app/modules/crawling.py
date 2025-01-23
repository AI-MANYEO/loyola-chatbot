from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import json

BASE_URL = "https://library.sogang.ac.kr/"

class SogangLibraryCrawler:
    def __init__(self):
        self.visited_urls = set()

    def fetch_page(self, url):
        """지정된 URL의 HTML을 가져와 BeautifulSoup 객체로 반환."""
        print(f"Fetching: {url}")
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def extract_table(self, table):
        """테이블을 추출하고, 병합된 셀을 풀어 정리."""
        columns = []
        rows = []
        
        # 컬럼명 추출
        for th in table.select("thead th"):
            colspan = int(th.get("colspan", 1))
            for _ in range(colspan):
                columns.append(th.get_text(strip=True))
        
        # 행 데이터 추출
        for row in table.select("tbody tr"):
            row_data = []
            tds = row.select("td")
            for i, td in enumerate(tds):
                colspan = int(td.get("colspan", 1))
                for _ in range(colspan):
                    row_data.append(td.get_text(strip=True))
            rows.append(row_data)
        
        # 컬럼과 행 데이터 결합
        structured_rows = []
        for row in rows:
            structured_row = {columns[i]: row[i] for i in range(len(columns))}
            structured_rows.append(structured_row)
        
        return structured_rows

    def crawl_page(self, url):
        """지정된 페이지에서 데이터를 크롤링."""
        if url in self.visited_urls:
            return {"url": url, "description": "Already visited", "content": []}
        
        self.visited_urls.add(url)
        soup = self.fetch_page(url)
        
        title = soup.find("h2", id="divTitle").get_text(strip=True) if soup.find("h2", id="divTitle") else "No Title"
        breadcrumbs = soup.select("#divLocation ul li a")
        category = breadcrumbs[1].get_text(strip=True) if len(breadcrumbs) > 1 else "No Category"
        subcategory = breadcrumbs[2].get_text(strip=True) if len(breadcrumbs) > 2 else "No Subcategory"
        
        description = []

        # ✅ 테이블 데이터 추가
        table = soup.select_one(".listTable table")
        if table:
            table_data = self.extract_table(table)
            description.append({"section": "Table Data", "content": table_data})

        # ✅ 가나다순 검색 정보 추가
        search_area = soup.select_one(".searchArea")
        if search_area:
            search_links = {a.get_text(strip=True): urljoin(BASE_URL, a["href"]) for a in search_area.select("a")}
            description.append({"section": "Search Area", "content": search_links})

        # ✅ 페이지 네비게이션 정보 추가
        paging = soup.select_one(".paging")
        if paging:
            page_info = paging.get_text(strip=True)
            description.append({"section": "Paging", "content": page_info})

        # ✅ 탭 탐색 (divTabMenu가 있는 경우 추가 크롤링)
        tab_links = {a.get_text(strip=True): urljoin(BASE_URL, a["href"]) for a in soup.select("#divTabMenu ul li a")}
        if tab_links:
            tabs_data = []
            for tab_name, tab_url in tab_links.items():
                if tab_url not in self.visited_urls:
                    tab_content = self.crawl_page(tab_url)  # ✅ 크롤링하여 전체 내용 저장
                    if tab_content and tab_content.get("description"):  # ✅ 내용이 있을 때만 추가
                        tabs_data.append({"tab_name": tab_name, "content": tab_content})
            if tabs_data:
                description.append({"section": "Tabs", "content": tabs_data})

        return {"category": category, "subcategory": subcategory, "url": url, "title": title, "description": description}

    def crawl_menu(self, url):
        """메뉴 구조를 크롤링하고, 각각의 페이지를 수집."""
        print("메뉴 크롤링 시작...")
        soup = self.fetch_page(url)
        menu_data = []
        
        for menu_item in soup.select("#divTopMenu ul li a"):
            href = menu_item["href"]
            full_url = urljoin(BASE_URL, href)
            
            try:
                page_data = self.crawl_page(full_url)
                menu_data.append(page_data)
            except Exception as e:
                print(f"Failed to crawl {full_url}: {e}")
        
        return menu_data

    def run(self):
        """크롤링 실행 및 데이터 저장."""
        menu_data = self.crawl_menu(BASE_URL)
        
        save_directory = "database/raw"
        os.makedirs(save_directory, exist_ok=True)
        
        with open(os.path.join(save_directory, "sogang_library_structured_oop.json"), "w", encoding="utf-8") as f:
            json.dump(menu_data, f, ensure_ascii=False, indent=4)
        
        print(f"크롤링 완료! {len(menu_data)}개의 메뉴를 수집했고, 데이터는 {save_directory}/sogang_library_structured.json에 저장되었습니다.")

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    crawler = SogangLibraryCrawler()
    crawler.run()
>>>>>>> origin/hyunjin
