import json
import os
import requests
from bs4 import BeautifulSoup

# 기본 URL 및 저장 디렉토리 설정
BASE_URL = "https://library.sogang.ac.kr"
SAVE_DIRECTORY = "database/raw"

class MenuItem:
    """메뉴 항목을 저장하는 데이터 클래스"""
    def __init__(self, category, subcategory, title, url):
        self.category = category
        self.subcategory = subcategory
        self.title = title
        self.url = url

    def to_dict(self):
        """객체를 딕셔너리 형태로 변환"""
        return vars(self)

class MenuScraper:
    """웹사이트의 메뉴 구조를 크롤링하는 클래스"""
    def __init__(self, url, save_directory=SAVE_DIRECTORY):
        self.url = url
        self.save_directory = save_directory
        self.menu_items = []
        os.makedirs(self.save_directory, exist_ok=True)

    def fetch_html(self):
        """웹페이지의 HTML을 가져오는 메서드"""
        print("Fetching HTML...")
        response = requests.get(self.url)
        response.raise_for_status()
        print("Successfully fetched HTML!")
        return response.text

    def extract_menu_items(self, section):
        """HTML 섹션에서 메뉴 항목을 추출하는 메서드"""
        category_tag = section.find("a")
        if not category_tag:
            return []
        category = category_tag.get("title", "").strip()

        menu_items = []
        subcategory_containers = section.find_all("ul")
        for subcategory_ul in subcategory_containers:
            subcategory_tag = subcategory_ul.find_previous("a")
            subcategory = subcategory_tag.get("title", "").strip() if subcategory_tag else ""

            if category == subcategory:
                continue

            for item in subcategory_ul.find_all("li"):
                link = item.find("a")
                if link:
                    title = link.get("title", "").strip()
                    url = BASE_URL + link.get("href", "").strip()
                    menu_items.append(MenuItem(category, subcategory, title, url))
        return menu_items

    def parse_menu(self, html):
        """HTML을 파싱하여 메뉴 정보를 추출하는 메서드"""
        print("Parsing menu structure...")
        soup = BeautifulSoup(html, 'html.parser')
        menu_sections = [soup.find_all("li", class_=f"wholeMenu{i}") for i in range(1, 7)]
        menu_sections = [item for sublist in menu_sections for item in sublist]
        
        for section in menu_sections:
            self.menu_items.extend(self.extract_menu_items(section))
        print(f"Parsed {len(self.menu_items)} menu items.")

    def save_to_json(self, filename):
        """추출한 데이터를 JSON 파일로 저장하는 메서드"""
        filepath = os.path.join(self.save_directory, filename)
        print(f"Saving data to {filepath}...")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in self.menu_items], f, ensure_ascii=False, indent=4)
        print("Data successfully saved!")

    def run(self):
        """크롤링 실행 및 데이터 저장."""
        html = self.fetch_html()
        self.parse_menu(html)
        self.save_to_json("menu_data.json")
        print(f"크롤링 완료! {len(self.menu_items)}개의 메뉴를 수집했고, 데이터는 {self.save_directory}/menu_data.json에 저장되었습니다.")

if __name__ == "__main__":
    scraper = MenuScraper(BASE_URL)
    scraper.run()
