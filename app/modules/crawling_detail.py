import os
import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# 기본 설정
BASE_URL = "https://library.sogang.ac.kr"
SAVE_DIRECTORY = "database/raw"
FILE_PATHS = {
    "menu": os.path.join(SAVE_DIRECTORY, "menu_data.json"),  # 🔹 메뉴 데이터 저장 파일
    "details": os.path.join(SAVE_DIRECTORY, "detail_data.json")  # 🔹 상세 정보 저장 파일
}

def clean_text(text):
    """불필요한 공백을 제거하고 숫자+한글 사이 띄어쓰기 수정 및 불필요한 문자 정리"""
    text = re.sub(r'\s+', ' ', text)  # 여러 개의 공백을 하나로 변환
    text = re.sub(r'(\d+)\s([가-힣])', r'\1\2', text)  # 숫자와 한글 사이 띄어쓰기 제거
    return text.strip()

"""⭐️ BaseScraper:공통적인 크롤링 기능을 제공하는 기본 클래스 ⭐️"""
class BaseScraper:
    def fetch_html(self, url):
        """주어진 URL에서 HTML을 가져오는 메서드"""
        print(f"Fetching HTML from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_html(self, html):
        """HTML을 BeautifulSoup 객체로 변환하는 메서드"""
        return BeautifulSoup(html, 'html.parser')

        # ✅ 외부 URL 추가 필터링 (BASE_URL이 포함되지 않은 절대 URL은 제외)
        if not url.startswith(BASE_URL+"/"):
            print(f"🚫 [DEBUG] 외부 및 절대 URL 감지: {url} -> 크롤링 제외.")
            return
            
    def is_valid_internal_url(self, url):
        """
        주어진 URL이 서강대 도서관 내부 URL인지 확인하는 함수.
        외부 사이트 및 절대 URL을 크롤링하지 않도록 필터링한다.
        
        :param url: 검사할 URL
        :return: True (유효한 내부 URL) / False (외부 URL 또는 잘못된 절대 URL)
        """
        # ✅ URL이 `BASE_URL`로 시작하는지 검사
        if url.startswith(BASE_URL + "/"):
            return True  # 내부 URL이므로 크롤링 가능
        
        # 🚫 외부 URL 감지 → 크롤링 제외
        print(f"🚫 [DEBUG] 외부 및 절대 URL 감지: {url} -> 크롤링 제외.")
        return False  # 외부 URL이므로 크롤링 제외

    def extract_text(self, soup, parent_tag, parent_class, text_tag, text_class="None"):
        """
        특정 부모 태그 또는 전체 문서에서 지정한 태그의 텍스트를 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (예: "div", "li")
        :param parent_class: 부모 태그 클래스 (예: "guide", None 가능)
        :param text_tag: 텍스트 태그 (예: "h3")
        :param text_class: 텍스트 태그 클래스 (예: "titleStyle1")
        :return: 텍스트 리스트
        """
        extracted_texts = []

        # ✅ 부모 태그가 주어졌다면 해당 범위에서 검색, 없으면 전체에서 검색
        if parent_class:
            parent_sections = soup.find_all(parent_tag, class_=parent_class)
        else:
            parent_sections = [soup]  # 전체 문서에서 검색

        for section in parent_sections:
            text_elements = section.find_all(text_tag, class_=text_class)
            for text_element in text_elements:
                extracted_texts.append(clean_text(text_element.text.strip()))

        return extracted_texts

    def extract_key_value(self, soup, parent_tag, parent_class, item_tag="li", key_tag="span"):
        """
        특정 부모 태그 내부에서 key-value 형태의 데이터를 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "contact2")
        :param item_tag: 개별 항목 태그 (기본값: "li")
        :param key_tag: 키를 포함하는 태그 (기본값: "span")
        :return: {key: value} 형태의 딕셔너리
        """
        extracted_data = {}

        parent_section = soup.find(parent_tag, class_=parent_class)
        if parent_section:
            items = parent_section.find_all(item_tag)
            for item in items:
                key_element = item.find(key_tag)
                key = clean_text(key_element.text.strip()) if key_element else ""
                
                # ✅ 이메일 주소 처리 (a 태그가 있는 경우)
                email_link = item.find("a")
                if email_link and "href" in email_link.attrs:
                    value = clean_text(email_link["href"].replace("mailto:", "").strip())
                else:
                    value = clean_text(item.text.replace(key, "").strip())

                if key:
                    extracted_data[key] = value  # key가 있으면 {key: value} 저장
                else:
                    extracted_data[f"기타_{len(extracted_data) + 1}"] = value  # key가 없으면 기타 항목 저장

        return extracted_data
    
    def extract_list(self, soup, parent_tag, parent_class, list_tag="li", list_class=None):
        """
        특정 부모 태그 내부에서 리스트 항목을 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "textBox2 type2")
        :param list_tag: 리스트 항목 태그 (기본값: "li")
        :param list_class: 리스트 항목 클래스 (기본값: None, 모든 li 선택 가능)
        :return: 리스트 텍스트 데이터 리스트
        """
        extracted_texts = []

        parent_section = soup.find(parent_tag, class_=parent_class)
        if parent_section:
            list_items = parent_section.find_all(list_tag, class_=list_class) if list_class else parent_section.find_all(list_tag)
            extracted_texts.extend([clean_text(item.get_text(separator=" ", strip=True)) for item in list_items])

        return extracted_texts


    def extract_nested_list(self, soup, parent_tag, parent_class, title_tag, title_class, list_tag, list_class, sub_list_tag, sub_list_class, numbered_list_class=None):
        """
        중첩된 리스트 데이터를 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "guide")
        :param title_tag: 최상위 제목 태그 (ex: "li")
        :param title_class: 최상위 제목 태그 클래스 (ex: "listStyle5")
        :param list_tag: 중간 목록 태그 (ex: "li")
        :param list_class: 중간 목록 태그 클래스 (ex: "listStyle5")
        :param sub_list_tag: 하위 목록 태그 (ex: "li")
        :param sub_list_class: 하위 목록 태그 클래스 (ex: "listStyle6")
        :param numbered_list_class: 번호 포함 목록 클래스 (ex: "numListWrap")
        :return: "최상위제목: 중간제목: 하위목록" 형태의 리스트
        """
        extracted_data = []

        parent_sections = soup.find_all(parent_tag, class_=parent_class)
        for section in parent_sections:
            sub_list_items = section.find_all(list_tag, class_=list_class)
            for sub_item in sub_list_items:
                title_text = clean_text(sub_item.get_text(strip=True))

                # ✅ 하위 목록 (listStyle6) 추출
                sub_descs = [clean_text(li.text.strip()) for li in sub_item.find_all(sub_list_tag, class_=sub_list_class)]

                # ✅ 번호 포함 리스트 (numListWrap) 처리
                num_list_texts = []
                if numbered_list_class:
                    num_list_items = sub_item.find_all("li", class_=numbered_list_class)
                    for num_list in num_list_items:
                        num_texts = []
                        for li in num_list.find_all("li"):
                            num_prefix = li.find("span", class_="numList")
                            if num_prefix:
                                num_texts.append(f"{num_prefix.text.strip()} {clean_text(li.text.replace(num_prefix.text, '').strip())}")
                            else:
                                num_texts.append(clean_text(li.text.strip()))
                        if num_texts:
                            num_list_texts.append(", ".join(num_texts))

                # ✅ 최종 데이터 저장
                if sub_descs:
                    extracted_data.append(f"{title_text}: {' '.join(sub_descs)}")
                if num_list_texts:
                    extracted_data.append(f"{title_text}: {' '.join(num_list_texts)}")

        return extracted_data
    
    @staticmethod
    def is_absolute_url(url):
        """주어진 URL이 절대 URL인지 확인하는 함수"""
        return bool(re.match(r"^(?:http|https)://", url)) 
    
    def extract_tabs(self, soup, menu_id, container_selector, category, subcategory, title):
        """
        탭 메뉴에서 탭 이름과 URL을 추출하여 중복 방지를 고려하면서 처리하는 함수.
        """
        tab_menu = soup.select(f"{menu_id} {container_selector}")

        for tab_item in tab_menu:
            tab_name = clean_text(tab_item.text.strip())
            tab_href = tab_item.get("href", "").strip()

            print(f"🔎 [DEBUG] 추출된 탭: {tab_name} | href: {tab_href}")  # ✅ href 디버깅

            # ✅ (1) 잘못된 href 필터링 (비어있거나 JavaScript 코드)
            if not tab_href or "javascript:void(0);" in tab_href:
                print(f"⚠️ 잘못된 href 감지: {tab_href} -> 건너뜀.")
                continue

            # ✅ (2) 절대 URL 판별 및 제외 (http:// 또는 https:// 로 시작하면 제외)
            if self.is_absolute_url(tab_href):
                print(f"🚫 [DEBUG] 절대 URL 감지: {tab_href} -> 크롤링 제외.")
                continue
            
            # ✅ (3) 상대 URL이면 BASE_URL과 결합
            tab_url = urljoin(BASE_URL, tab_href) if not self.is_absolute_url(tab_href) else tab_href


            print(f"🔗 [DEBUG] 최종 변환된 tab_url: {tab_url}")  # ✅ 변환된 URL 디버깅

            # ✅ 중복 URL 확인
            if tab_url in self.processed_tabs and tab_name in self.processed_tabs[tab_url]:
                print(f"⚠️ [DEBUG] 이미 처리된 탭: {tab_name} ({tab_url}) -> 건너뜀.")
                continue

            # ✅ 정상적인 탭 URL이면 크롤링 진행
            print(f"🔄 [DEBUG] 탭 이동: {tab_name} ({tab_url})")
            self.parse_detail(tab_url, category, subcategory, title, tab_name)

            # ✅ 중복 URL이더라도 탭 이름이 다르면 저장
            if tab_url not in self.processed_tabs:
                self.processed_tabs[tab_url] = set()
            self.processed_tabs[tab_url].add(tab_name)

    def extract_qna(self, soup, parent_tag, parent_class, item_tag="li", question_tag="h5", question_class="qnaTitle", answer_tag="div", answer_class="qnaText"):
        """
        특정 부모 태그 내부에서 QnA 형태의 데이터를 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "ul")
        :param parent_class: 부모 태그 클래스 (ex: "qnaWrap")
        :param item_tag: 개별 QnA 항목 태그 (기본값: "li")
        :param question_tag: 질문 태그 (기본값: "h5")
        :param question_class: 질문 태그 클래스 (기본값: "qnaTitle")
        :param answer_tag: 답변 태그 (기본값: "div")
        :param answer_class: 답변 태그 클래스 (기본값: "qnaText")
        :return: ["Q: 질문 내용 A: 답변 내용"] 형태의 리스트
        """
        extracted_qna = []

        parent_section = soup.find(parent_tag, class_=parent_class)
        if parent_section:
            qna_items = parent_section.find_all(item_tag)
            for qna in qna_items:
                # ✅ 질문 처리 (a > span 내부 텍스트 추출)
                question_element = qna.find(question_tag, class_=question_class)
                question_span = question_element.find("a").find("span") if question_element and question_element.find("a") else None
                question = clean_text(question_span.text.strip()) if question_span else None

                # ✅ 답변 처리 (여러 <p> 태그가 존재할 수 있음)
                answer_element = qna.find(answer_tag, class_=answer_class)
                if answer_element:
                    answer_paragraphs = answer_element.find_all("p")  # 여러 <p> 태그가 있을 경우
                    if answer_paragraphs:
                        answer = " ".join([clean_text(p.text.strip()) for p in answer_paragraphs])
                    else:
                        answer = clean_text(answer_element.text.strip())  # <p> 태그가 없으면 전체 텍스트 가져오기
                else:
                    answer = None

                # ✅ 최종 데이터 저장
                if question and answer:
                    extracted_qna.append(f"Q: {question} A: {answer}")

        return extracted_qna
        
    def extract_faq(self, soup, parent_tag="dl", parent_class="faqList", question_tag="dt", answer_tag="dd"):
        """
        FAQ 형태의 데이터를 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: FAQ 전체를 감싸는 부모 태그 (기본값: "dl")
        :param parent_class: 부모 태그의 클래스명 (기본값: "faqList")
        :param question_tag: 질문 태그 (기본값: "dt")
        :param answer_tag: 답변 태그 (기본값: "dd")
        :return: ["Q: 질문 내용 A: 답변 내용"] 형태의 리스트
        """
        extracted_faq = []

        parent_section = soup.find(parent_tag, class_=parent_class)
        if parent_section:
            question_elements = parent_section.find_all(question_tag)
            answer_elements = parent_section.find_all(answer_tag)
        

            if len(question_elements) != len(answer_elements):
                print(f"⚠️ [DEBUG] 질문과 답변 개수 불일치! ({len(question_elements)} vs {len(answer_elements)})")

            for question_element, answer_element in zip(question_elements, answer_elements):
                # ✅ 질문 추출
                question_link = question_element.find("a")
                question = clean_text(question_link.text.strip()) if question_link else None

                # ✅ 답변 추출
                answer = clean_text(answer_element.text.strip()) if answer_element else None

                # ✅ 데이터 저장
                if question and answer:
                    extracted_faq.append(f"Q: {question} A: {answer}")

        return extracted_faq
    def extract_faq_tabs(self, soup, base_url):
        """
        FAQ 페이지에서 탭(카테고리) 정보를 추출하여 각각 크롤링하는 함수.

        :param soup: BeautifulSoup 객체
        :param base_url: 상대 경로를 절대 URL로 변환하기 위한 기본 URL
        """
        faq_tab_section = soup.find("div", class_="faqTab")
        if not faq_tab_section:
            return

        # ✅ FAQ 탭 리스트 찾기
        tab_links = faq_tab_section.select("ul.on li a")

        for tab in tab_links:
            tab_name = clean_text(tab.text.strip())  # ✅ 탭 이름
            tab_href = tab.get("href", "").strip()  # ✅ URL

            # 🚫 잘못된 URL 필터링 (JavaScript 또는 빈 값)
            if not tab_href or "javascript:void(0);" in tab_href:
                print(f"⚠️ [DEBUG] 잘못된 FAQ 탭 URL 감지: {tab_href} -> 건너뜀")
                continue

            # ✅ 절대 URL 처리
            tab_url = urljoin(base_url, tab_href)

            # 🚫 외부 URL 크롤링 방지 (is_valid_internal_url 사용)
            if not self.is_valid_internal_url(tab_url):
                continue  # ⚠️ is_valid_internal_url 내부에서 디버그 메시지 출력됨.

            # ✅ 중복 방지
            if tab_url in self.processed_urls:
                print(f"⚠️ [DEBUG] 이미 방문한 FAQ 탭: {tab_name} ({tab_url}) -> 건너뜀")
                continue

            print(f"🔄 [DEBUG] FAQ 탭 이동: {tab_name} ({tab_url})")

            # ✅ FAQ 페이지 크롤링 시작
            html = self.fetch_html(tab_url)
            tab_soup = self.parse_html(html)

            # ✅ 해당 탭의 FAQ 데이터 수집
            self.parse_detail(tab_url, "FAQ", "", tab_name, tab_name, tab_soup)



    def extract_table(self, soup, parent_tag="div", parent_class="guideTable type2", table_tag="table"):
        """
        HTML 테이블 데이터를 구조화하여 리스트 형태로 추출하는 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "guideTable type2")
        :param table_tag: 테이블 태그 (기본값: "table")
        :return: [{"구분": "대상", "학부생": "재학생, 휴학생, 수료생", "대학원생": "재학생, 휴학생, 수료생", "바로가기": "링크 URL"}] 형태의 리스트
        """
        parent_section = soup.find(parent_tag, class_=parent_class)
        if not parent_section:
            return []

        table = parent_section.find(table_tag)
        if not table:
            return []

        columns = []
        rows = []

        # ✅ 컬럼명 추출 (thead)
        thead = table.find("thead")
        if thead:
            for th in thead.find_all("th"):
                col_span = int(th.get("colspan", 1))
                text = clean_text(th.get_text(strip=True))
                for _ in range(col_span):
                    columns.append(text)

        # ✅ 행 데이터 추출 (tbody)
        tbody = table.find("tbody")
        if tbody:
            for row in tbody.find_all("tr"):
                row_data = []
                tds = row.find_all("td")

                for td in tds:
                    col_span = int(td.get("colspan", 1))
                    text = clean_text(td.get_text(strip=True))

                    # ✅ "바로가기" 열의 링크 추출
                    link = td.find("a")
                    if link:
                        text = f"{text} ({urljoin(BASE_URL, link.get('href'))})"

                    for _ in range(col_span):
                        row_data.append(text)

                rows.append(row_data)

        # ✅ 컬럼 개수와 데이터 개수가 맞지 않으면 스킵
        structured_rows = []
        for row in rows:
            if len(row) != len(columns):
                continue  # ⚠️ 컬럼 개수와 다르면 추가하지 않음

            structured_row = {columns[i]: row[i] for i in range(len(columns))}
            structured_rows.append(structured_row)

        return structured_rows


    def extract_links(self, soup, parent_tag, parent_class, title_tag, title_class, link_tag, link_class, base_url):
        """
        부모 태그 내부에서 제목과 링크를 추출하는 범용 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "collectionItem")
        :param title_tag: 제목 태그 (ex: "a")
        :param title_class: 제목 태그 클래스 (ex: "")
        :param link_tag: 링크 태그 (ex: "a")
        :param link_class: 링크 태그 클래스 (ex: "")
        :param base_url: 사이트의 기본 URL (상대 경로를 절대 URL로 변환하기 위해 필요)
        :return: [{"title": "제목", "url": "링크"}] 형태의 리스트
        """
        extracted_data = []
        parent_sections = soup.find_all(parent_tag, class_=parent_class)

        for section in parent_sections:
            title_element = section.find(title_tag, class_=title_class)
            title_text = clean_text(title_element.text.strip()) if title_element else "Unknown"

            links = []
            for link in section.find_all(link_tag, class_=link_class):
                link_text = clean_text(link.text.strip())
                link_url = urljoin(base_url, link.get("href", "").strip())

                if not link_url or "javascript:void(0);" in link_url:
                    continue  # ✅ 유효하지 않은 링크는 스킵

                links.append({"title": link_text, "url": link_url})

            # ✅ 제목 + 링크 리스트를 저장
            extracted_data.append({"category": title_text, "links": links})

        return extracted_data


    def extract_contact_info(self, soup, parent_tag="div", parent_class="textBox", contact_tag="ul", contact_class="contact", field_map=None):
        """
        범용적인 연락처 정보 추출 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (예: "div")
        :param parent_class: 부모 태그 클래스 (예: "textBox")
        :param contact_tag: 연락처 정보를 포함한 태그 (예: "ul")
        :param contact_class: 연락처 태그의 클래스 (예: "contact")
        :param field_map: 특정 키워드를 기준으로 데이터를 저장할 매핑 (예: {"위치": "관", "팩스": "Fax)", "전화번호": "tel"})
        :return: {"위치": "...", "전화번호": "...", "팩스": "...", "이메일": "..."} 형태의 딕셔너리
        """
        if field_map is None:
            field_map = {
                "위치": "관",
                "팩스": "Fax)",
                "전화번호": "tel",
                "이메일": "@"
            }

        contact_info = {}
        parent_section = soup.find(parent_tag, class_=parent_class)
        if parent_section:
            contact_section = parent_section.find(contact_tag, class_=contact_class)
            if contact_section:
                for li in contact_section.find_all("li"):
                    text = clean_text(li.get_text(strip=True))

                    # ✅ 이메일 처리
                    if field_map["이메일"] in text:
                        email_link = li.find("a")
                        if email_link:
                            contact_info["이메일"] = email_link.get("href").replace("mailto:", "").strip()
                        continue  # 이메일을 찾으면 다른 필드 매칭 건너뜀

                    # ✅ field_map 기준으로 값 매핑
                    for field, keyword in field_map.items():
                        if keyword in text:
                            contact_info[field] = text.replace(keyword, "").strip()

        return contact_info if contact_info else None


    def process_links_and_crawl(self, soup, parent_tag, parent_class, title_tag, title_class, link_tag, link_class, base_url, category, subcategory, title):
        """
        `extract_links()`를 활용하여 추출된 링크를 새로운 탭처럼 크롤링하는 범용 함수.

        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (ex: "div")
        :param parent_class: 부모 태그 클래스 (ex: "collectionItem")
        :param title_tag: 제목 태그 (ex: "a")
        :param title_class: 제목 태그 클래스 (ex: "")
        :param link_tag: 링크 태그 (ex: "a")
        :param link_class: 링크 태그 클래스 (ex: "")
        :param base_url: 사이트의 기본 URL
        :param category: 현재 페이지의 카테고리
        :param subcategory: 현재 페이지의 서브 카테고리
        :param title: 현재 페이지의 제목
        """
        extracted_links = self.extract_links(soup, parent_tag, parent_class, title_tag, title_class, link_tag, link_class, base_url)

        for link_data in extracted_links:
            tab_name = link_data["category"]  # ✅ 제목을 탭 이름으로 사용

            for link in link_data["links"]:
                tab_url = link["url"]

                # ✅ 외부 URL 필터링 적용!
                if not self.is_valid_internal_url(tab_url):
                    print(f"🚫 [DEBUG] 외부 URL 감지: {tab_url} -> 크롤링 제외.")
                    continue

                # ✅ 중복된 URL 크롤링 방지
                if tab_url in self.processed_urls:
                    print(f"⚠️ [DEBUG] 중복된 링크: {tab_name} ({tab_url}) -> 스킵")
                    continue

                print(f"🔄 [DEBUG] 이동: {tab_name} ({tab_url})")
                html = self.fetch_html(tab_url)
                self.parse_detail(tab_url, category, subcategory, title, tab_name)

    def extract_db_table(self, soup, parent_tag, parent_class, base_url):
        """
        학술 DB 관련 테이블 데이터를 추출하는 함수.
        
        :param soup: BeautifulSoup 객체
        :param parent_tag: 부모 태그 (예: "div")
        :param parent_class: 부모 태그 클래스 (예: "guideTable type2 db1 mt0")
        :param base_url: 상대 URL을 절대 URL로 변환하기 위한 기본 URL
        :return: [{"db_name": "DB명", "description": "DB 설명", "url": "DB 링크"}] 형태의 리스트
        """
        extracted_data = []

        # ✅ 테이블이 포함된 부모 div 찾기
        parent_section = soup.find(parent_tag, class_=parent_class)
        if not parent_section:
            return extracted_data  # 테이블이 없으면 빈 리스트 반환

        table = parent_section.find("table", class_="mobileTable")
        if not table:
            return extracted_data  # 테이블이 없으면 빈 리스트 반환

        tbody = table.find("tbody")
        if not tbody:
            return extracted_data  # tbody가 없으면 빈 리스트 반환

        # ✅ 테이블의 각 행을 반복하면서 데이터 추출
        for row in tbody.find_all("tr"):
            columns = row.find_all("td")

            if len(columns) < 2:
                continue  # 최소한 2개의 컬럼(DB명, 설명)이 필요

            # ✅ DB명 (첫 번째 열, a 태그 내부 텍스트)
            db_link_tag = columns[0].find("a")
            db_name = clean_text(db_link_tag.text.strip()) if db_link_tag else clean_text(columns[0].text.strip())
            db_url = urljoin(base_url, db_link_tag["href"]) if db_link_tag and db_link_tag.get("href") else None

            # ✅ DB 설명 (두 번째 열)
            description_list = [clean_text(span.text.strip()) for span in columns[1].find_all("span", class_="tableList")]
            description = " ".join(description_list) if description_list else clean_text(columns[1].text.strip())

            # ✅ 최종 데이터 추가
            extracted_data.append({
                "db_name": db_name,
                "description": description,
                "url": db_url if db_url else "URL 없음"
            })

        return extracted_data




"""⭐️ DetailScraper: 상세 페이지 정보를 크롤링하는 클래스 ⭐️"""
class DetailScraper(BaseScraper):
    def __init__(self, urls, data_manager):
        self.urls = urls
        self.details = []
        self.processed_urls = set()
        self.processed_tabs = {}
        self.data_manager = data_manager # ✅ DataManager 인스턴스 사용

    def parse_detail(self, url, category, subcategory, title, tab, soup=None):
        """HTML을 파싱하여 상세 정보를 추출"""  

        # 🚫 외부 URL 크롤링 차단
        if not self.is_valid_internal_url(url):  # ✅ 내부 URL인지 검사
            return  # 크롤링 제외 (메시지는 이미 `is_valid_internal_url`에서 출력됨)

        
        # ✅ 중복 URL & 탭 확인
        if url in self.processed_urls and tab in self.processed_tabs.get(url, set()):
            print(f"⏩ [DEBUG] 이미 방문한 URL: {url} (탭: {tab}) -> 건너뜀.")
            return

        # ✅ URL 크롤링 처리 시작
        print(f"🔍 [DEBUG] 크롤링 시작: {url} (탭: {tab})")
        self.processed_urls.add(url)
        if url not in self.processed_tabs:
            self.processed_tabs[url] = set()
        self.processed_tabs[url].add(tab)

        # ✅ HTML 가져오기
        html = self.fetch_html(url)
        soup = self.parse_html(html)
        
        descriptions = []
        
        # ✅ `collectionItem` 내부 링크 처리
        self.process_links_and_crawl(
            soup, "div", "collectionItem", "a", "", "a", "", BASE_URL, 
            category, subcategory, title
        )

        # ✅ `guide` 내부 `linkStyle3` 링크 처리
        self.process_links_and_crawl(
            soup, "div", "guide", "h4", "titleStyle1", "a", "linkStyle3", BASE_URL, 
            category, subcategory, title
        )

        # ✅ `guide` 내부 `linkStyle2` 링크 처리
        self.process_links_and_crawl(
            soup, "div", "guide", "h4", "titleStyle1", "a", "linkStyle2", BASE_URL, 
            category, subcategory, title
        )

        # ✅ `faqTab` 내부 링크 처리
        self.process_links_and_crawl(
            soup, "div", "faqTab", "ul", "on", "a", "", BASE_URL, 
            category, subcategory, title
        )
        # ✅ `faqTab` 내부 링크 처리
        self.process_links_and_crawl(
            soup, "div", "faqTab", "ul", "on", "a", "", BASE_URL, 
            category, subcategory, title
        )



        # ✅ 일반 텍스트 정보 수집 (`collectionInfo`)
        descriptions = self.extract_text(soup, "div", "collectionInfo", "div", "info")

        # ✅ `searchInfoBox` 데이터 수집 (제목 h3)
        descriptions.extend(self.extract_text(soup, "div", "searchInfoBox", "h3", "searchTitle1"))  # 제목 추출

        # ✅ `searchInfoBox` 데이터 수집 (내용 ul)
        descriptions.extend(self.extract_list(soup, "div", "searchInfoBox", "ul"))  # 리스트 추출

        # ✅ `guide` 내부 `textBox2.type2` (제목 h3)
        descriptions.extend(self.extract_text(soup, "div", "textBox2 type2", "h3", "textBoxTitle"))  # 제목 추출

        # ✅ `guide` 내부 `textBox2.type2` (내용 p)
        descriptions.extend(self.extract_list(soup, "div", "textBox2 type2", "p"))  # 본문 추출

        # ✅ `guide` 내부 list 구조 (제목 h4)
        descriptions.extend(self.extract_text(soup, "div", "guide", "h4", "titleStyle1"))  # ✅ 제목(`h4.titleStyle1`) 추출

        # ✅ `guide` 내부 list 구조 (목록 li.listStyle5)
        descriptions.extend(self.extract_list(soup, "div", "guide", "li", "listStyle5"))  # ✅ 리스트(`li.listStyle5`) 추출

        # ✅ 설명 텍스트 ('textBox3.type1' 내부 listStyle4 리스트)
        descriptions.extend(self.extract_text(soup, "div", "textBox3 type1", "p", "listStyle4"))

        # ✅ 설명 텍스트 (`textBox2.type2` 내부 listStyle5 리스트)
        descriptions.extend(self.extract_list(soup, "div", "textBox2 type2", "li", "listStyle5"))

        # ✅ `listStyle5` + `listStyle6` 중첩 리스트 처리
        descriptions.extend(
            self.extract_nested_list(
                soup,
                parent_tag="div", parent_class="guide",
                title_tag="li", title_class="listStyle5",
                list_tag="li", list_class="listStyle5",
                sub_list_tag="li", sub_list_class="listStyle6"
            )
        )

        # ✅ `EndNote, 기능 및 특징` 데이터 수집 (중첩 리스트 처리)
        descriptions.extend(
            self.extract_nested_list(
                soup,
                parent_tag="div", parent_class="guide",
                title_tag="h3", title_class="titleStyle1",
                list_tag="li", list_class="listStyle5",
                sub_list_tag="li", sub_list_class="listStyle6",
                numbered_list_class="numListWrap"
            )
        )

        # ✅ QnA 정보 (`qnaWrap` 내부 질문-답변 구조)
        descriptions.extend(self.extract_qna(soup, "ul", "qnaWrap"))
        
        # ✅ 문의 정보 (`contact2` 내부 key-value 구조)
        contact_info = self.extract_key_value(soup, "div", "contact2")
        
        # ✅ 교육 신청 및 문의 정보 (`contentHeader` 내부 모든 li 리스트)
        descriptions.extend(self.extract_list(soup, "div", "contentHeader"))
        
        # ✅ FAQ 탭 크롤링 (탭 이동 후 해당 페이지의 FAQ 데이터 수집)
        self.extract_faq_tabs(soup, BASE_URL)

        # ✅ FAQ 데이터 추출
        faq_data = self.extract_faq(soup, "dl", "faqList")

        # ✅ FAQ 데이터를 descriptions 리스트에 추가
        if faq_data:
            descriptions.extend(faq_data)

        # ✅ 일반 텍스트 정보 수집
        descriptions.extend(self.extract_text(soup, "div", "textBox", "p"))

        # ✅ 연락처 정보 추출 
        contact_info = self.extract_contact_info(
            soup,
            parent_tag="div",
            parent_class="textBox",
            contact_tag="ul",
            contact_class="contact",
            field_map={
                "위치": "관",
                "팩스": "Fax)",
                "전화번호": "tel",
                "이메일": "@"
            }
        )
<<<<<<< HEAD
        
        # ✅ 연
=======
>>>>>>> origin/sorin

        # ✅ 테이블 데이터 추출 (guideTable type2)
        table_data = self.extract_table(soup, "div", "guideTable type2", "table")
        if table_data:
            descriptions.extend(table_data)  # ✅ 테이블 데이터를 description에 추가

        # ✅ `mobileTable` 데이터 추출
        mobile_table_data = self.extract_table(soup, "table", "mobileTable")
        if mobile_table_data:
            descriptions.extend(mobile_table_data)  # ✅ mobileTable 데이터를 description에 추가

        # ✅ 학술 DB 테이블 정보 추출
        db_table_data = self.extract_db_table(soup, "div", "guideTable type2 db1 mt0", BASE_URL)
        if db_table_data:
            for db in db_table_data:
                self.details.append({
                    "category": category,
                    "subcategory": subcategory,
                    "title": title,
                    "tab": tab,
                    "url": url,
                    "description": f"{db['db_name']} - {db['description']}",
                    "contact": contact_info if contact_info else None
                })
                
        # ✅ "titleStyle1" 텍스트 추출
        title_texts = self.extract_text(soup, "li", None, "h3", "titleStyle1")
        if title_texts:
            descriptions.extend(title_texts)  # ✅ "이용방법" 같은 제목을 description에 추가



        # ✅ `.listTable table` 데이터 추출
        table_data = self.extract_table(soup, "div", "listTable", "table")  # ✅ 태그 & 클래스 방식으로 변경
        if table_data:
            for row in table_data:
                self.details.append({
                    "category": category,
                    "subcategory": subcategory,
                    "title": title,
                    "tab": tab,
                    "url": url,
                    "description": row,  # ✅ 테이블 데이터를 description에 저장
                    "contact": contact_info if contact_info else None
                })
        else:
            # ✅ 테이블이 없을 경우 일반 설명 데이터 저장
            self.details.append({
                "category": category,
                "subcategory": subcategory,
                "title": title,
                "tab": tab,
                "url": url,
                "description": descriptions,
                "contact": contact_info if contact_info else None
            })


        # ✅ 탭 메뉴 크롤링 (중복 방지 적용)
        self.extract_tabs(soup, "#divTabMenu", "ul li a", category, subcategory, title)
        self.extract_tabs(soup, "#divTabMenu2", "ul.mTSContainer li a", category, subcategory, title)
        

    def run(self):
        """모든 URL을 크롤링하고 데이터를 저장하는 메서드"""
        if not self.urls or not isinstance(self.urls, list):  # ✅ URL 목록이 유효한지 확인
            print("⚠️ 유효한 URL 목록이 없습니다. 실행을 중단합니다.")
            return

        for entry in self.urls:
            # ✅ entry가 None이거나 리스트/튜플이 아닌 경우 건너뛰기
            if not isinstance(entry, (list, tuple)) or len(entry) < 5:
                print(f"⚠️ 데이터 형식 오류: {entry} (5개 요소 필요)")
                continue

            url, category, subcategory, title, tab = entry

            # ✅ URL 유효성 검사
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                print(f"⚠️ 잘못된 URL 감지: {url}, 크롤링 건너뜀.")
                continue

            # ✅ 상세 정보 크롤링 실행
            self.parse_detail(url, category, subcategory, title, tab)

        # ✅ 크롤링된 데이터가 있는 경우에만 저장
        if self.details:
            self.data_manager.save_to_json(self.details)
            print(f"✅ {len(self.details)}개의 데이터를 저장 완료!")
        else:
            print("⚠️ 크롤링된 데이터가 없어 저장하지 않습니다.")



"""⭐️ DataManager: 데이터 저장 및 로드 기능을 담당하는 클래스 ⭐️"""
class DataManager:
    def __init__(self, file_key):
        """
        :param file_key: `FILE_PATHS` 딕셔너리의 키값 (예: "menu", "details")
        """
        self.filepath = FILE_PATHS.get(file_key, None)
        if not self.filepath:
            raise ValueError(f"❌ Invalid file key: {file_key}. Available keys: {list(FILE_PATHS.keys())}")

        os.makedirs(SAVE_DIRECTORY, exist_ok=True)

    def save_to_json(self, data):
        """데이터를 JSON 파일로 저장 (중복 제거 후)"""
        print(f"💾 Saving data to {self.filepath}...")
        
        # ✅ 중복 제거 로직 적용 후 저장
        cleaned_data = self.remove_duplicate_entries(data)
        
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        
        print("✅ Data successfully saved!")

    def load_from_json(self):
        """JSON 파일에서 데이터를 로드"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def remove_duplicate_entries(self, data):
        """
        중복된 데이터에서 탭이 있는 경우만 남기는 함수.
        """
        filtered_data = []
        grouped_data = {}

        # 1️⃣ 같은 category, subcategory, title, url 기준으로 그룹화
        for entry in data:
            key = (entry["category"], entry["subcategory"], entry["title"], entry["url"])
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(entry)

        # 2️⃣ 그룹 내에서 'tab' 값이 있는 경우만 남김
        for key, entries in grouped_data.items():
            tab_entries = [e for e in entries if e["tab"]]  # 'tab'이 있는 데이터 필터링
            if tab_entries:
                filtered_data.extend(tab_entries)  # 'tab' 있는 데이터만 추가
            else:
                filtered_data.extend(entries)  # 'tab'이 없는 데이터만 있는 경우 유지

        return filtered_data  # ✅ 중복 제거된 데이터 반환



"""⭐️ 실행 코드 ⭐️"""
if __name__ == "__main__":
    data_manager_menu = DataManager("menu")  # 🔹 메뉴 데이터 관리 객체
    urls = [
        (item["url"], item["category"], item["subcategory"], item["title"], item.get("tab", ""))  # 🔹 tab 기본값 설정
        for item in data_manager_menu.load_from_json()
    ]

    data_manager_details = DataManager("details")  # 🔹 상세 정보 저장을 위한 DataManager 인스턴스 생성

    scraper = DetailScraper(urls, data_manager_details)  # ✅ DataManager를 `DetailScraper`에 주입
    scraper.run()

    # ✅ 크롤링된 데이터를 저장할 때 자동으로 중복 제거됨
    data_manager_details.save_to_json(scraper.details)

