import os
import re
import json
import requests
from bs4 import BeautifulSoup

class FileManager:
    """파일 관리 클래스"""
    @staticmethod
    def sanitize_filename(filename):
        """파일 이름에서 금지된 문자 제거"""
        return re.sub(r'[\\/:*?"<>|]', '_', filename)

    @staticmethod
    def save_to_json(data, filename):
        """JSON 데이터를 파일로 저장"""
        filename = FileManager.sanitize_filename(filename)
        base_dir = "crawled_data_oop"
        os.makedirs(base_dir, exist_ok=True)
        filepath = os.path.join(base_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

class Crawler:
    """크롤러 클래스"""
    def __init__(self):
        pass

    def crawl_page(self, url):
        """단일 페이지 크롤링"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        content = soup.find("div", id="divContents")
        if not content:
            return "크롤링할 내용이 없습니다."

        texts = []
        tables = []

        for tag in content.find_all(["p", "h3", "li", "ul"], recursive=True):
            if tag.text.strip():
                if not any(existing_item in tag.text.strip() or tag.text.strip() in existing_item for existing_item in texts):
                    texts.append(tag.text.strip())

        for table in content.find_all("table", recursive=True):
            tables.append(str(table))

        return {
            "texts": texts,
            "tables": tables
        }

    def crawl_submenus(self, menu, url):
        """세부 메뉴 크롤링"""
        data = {"메뉴": menu, "내용": []}
        main_content = self.crawl_page(url)
        data["내용"].append(main_content)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        submenu_links = soup.select("div#divTabMenu a")

        for link in submenu_links:
            submenu_name = link.text.strip()
            submenu_url = link["href"]
            if not submenu_url.startswith("http"):
                submenu_url = requests.compat.urljoin(url, submenu_url)
            submenu_content = self.crawl_page(submenu_url)
            data["내용"].append({submenu_name: submenu_content})

        return data

class CrawlerRunner:
    """크롤링 실행 관리 클래스"""
    def __init__(self, url_data):
        self.url_data = url_data
        self.crawler = Crawler()

    def run(self):
        """크롤링 실행"""
        for category in self.url_data:
            category_name = category["대분류"]
            for sub_category in category["소분류"]:
                sub_category_name = sub_category["이름"]
                url = sub_category["URL"]
                filename = f"database/raw{category_name}_{sub_category_name}.json"

                print(f"크롤링 중: {category_name} > {sub_category_name}")
                if "세부메뉴" in sub_category:
                    result = self.crawler.crawl_submenus(f"{category_name} > {sub_category_name}", url)
                else:
                    result = {"메뉴": f"{category_name} > {sub_category_name}", "내용": self.crawler.crawl_page(url)}

                FileManager.save_to_json(result, filename)

        print("크롤링 완료!")

# Example usage

# URL 데이터
url_data = [
    {
        "대분류": "도서관 소개",
        "중분류": "알림/문의",
        "소분류": [
            {"이름": "FAQ", "URL": "https://library.sogang.ac.kr/faqlib/faq?code=all"}
        
        ]
    },
    {
        "대분류": "자료검색",
        "중분류": "Browse",
        "소분류": [
            {"이름": "학술DB", "URL": "https://library.sogang.ac.kr/datalist/ejs/list"},
            {"이름": "학술DB 2p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=2"},
            {"이름": "학술DB 3p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=3"},
            {"이름": "학술DB 4p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=4"},
            {"이름": "학술DB 5p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=5"},
            {"이름": "학술DB 6p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=6"},
            {"이름": "학술DB 7p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=7"},
            {"이름": "학술DB 8p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=8"},
            {"이름": "학술DB 9p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=9"},
            {"이름": "학술DB 10p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=10"},
            {"이름": "학술DB 11p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=11"},
            {"이름": "학술DB 12p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=12"},
            {"이름": "학술DB 13p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=13"},
            {"이름": "학술DB 14p", "URL": "https://library.sogang.ac.kr/datalist/ejs/list?pn=14"},

            {"이름": "동영상 강좌", "URL": "https://library.sogang.ac.kr/datalist/vod/list"}
        ]
    },
    {
        "대분류": "로욜라 컬렉션",
        "중분류": "추천",
        "소분류": [
            {"이름": "인기자료", "URL": "https://library.sogang.ac.kr/favorloan/main?type=NEAR_MONTH&count=20"},
            {"이름": "신착자료", "URL": "https://library.sogang.ac.kr/newarrival"},
            {"이름": "신착자료 2p", "URL": "https://library.sogang.ac.kr/newarrival?pn=2"},
            {"이름": "신착자료 3p", "URL": "https://library.sogang.ac.kr/newarrival?pn=3"},
            {"이름": "신착자료 4p", "URL": "https://library.sogang.ac.kr/newarrival?pn=4"},
            {"이름": "신착자료 5p", "URL": "https://library.sogang.ac.kr/newarrival?pn=5"},
            {"이름": "신착자료 6p", "URL": "https://library.sogang.ac.kr/newarrival?pn=6"},
            {"이름": "신착자료 7p", "URL": "https://library.sogang.ac.kr/newarrival?pn=7"},
            {"이름": "신착자료 8p", "URL": "https://library.sogang.ac.kr/newarrival?pn=8"},
            {"이름": "신착자료 9p", "URL": "https://library.sogang.ac.kr/newarrival?pn=9"},
            {"이름": "신착자료 10p", "URL": "https://library.sogang.ac.kr/newarrival?pn=10"},
            {"이름": "신착자료 11p", "URL": "https://library.sogang.ac.kr/newarrival?pn=11"},
            {"이름": "신착자료 12p", "URL": "https://library.sogang.ac.kr/newarrival?pn=12"},
            {"이름": "신착자료 13p", "URL": "https://library.sogang.ac.kr/newarrival?pn=13"},
            {"이름": "신착자료 14p", "URL": "https://library.sogang.ac.kr/newarrival?pn=14"},
            {"이름": "신착자료 15p", "URL": "https://library.sogang.ac.kr/newarrival?pn=15"},
            {"이름": "신착자료 16p", "URL": "https://library.sogang.ac.kr/newarrival?pn=16"},
            {"이름": "신착자료 17p", "URL": "https://library.sogang.ac.kr/newarrival?pn=17"},
        ]
    },
    {
        "대분류": "로욜라 컬렉션",
        "중분류": "테마",
        "소분류": [
            {"이름": "서강필독서", "URL": "https://library.sogang.ac.kr/digicol/list/1"},# 검색기능 달려있음
            {"이름": "본교교수 저작물", "URL": "https://library.sogang.ac.kr/digicol/list/42"},# 검색기능 달려있음
            {"이름": "CGSI 기업연구 자료", "URL": "https://library.sogang.ac.kr/digicol/list/41"},# 검색기능 달려있음
            {"이름": "학위논문", "URL": "https://dcollection.sogang.ac.kr/dcollection/"}, #외부링크로 연결
            {"이름": "취업·창업도서", "URL": "https://library.sogang.ac.kr/digicol/list/2"},# 검색기능 달려있음
            {"이름": "학술원 우수학술도서", "URL": "https://library.sogang.ac.kr/digicol/list/82"}# 검색기능 달려있음
        ]
    },
    {
        "대분류": "연구학습지원",
        "중분류": "지정자료",
        "소분류": [
            {"이름": "지정자료신청", "URL": "https://library.sogang.ac.kr/htmlmanager/service/81"}
        ]
    },
    {
        "대분류": "연구학습지원",
        "중분류": "정보활용교육",
        "소분류": [
            {"이름": "교육안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/3"}
        ]
    },
    {
        "대분류": "연구학습지원",
        "중분류": "연구지원",
        "소분류": [
            {"이름": "연구가이드", "URL": "https://library.sogang.ac.kr/htmlmanager/service/4"},#
            {"이름": "연구가이드 공통 주제 국내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/823"},# 외부링크 달려있음
            {"이름": "연구가이드 공통 주제 국외", "URL": "https://library.sogang.ac.kr/htmlmanager/service/824"},
            {"이름": "연구가이드 학과/주제별 인문과학", "URL": "https://library.sogang.ac.kr/htmlmanager/service/828"},
            {"이름": "연구가이드 학과/주제별 사회과학", "URL": "https://library.sogang.ac.kr/htmlmanager/service/827"},
            {"이름": "연구가이드 학과/주제별 경제·경영", "URL": "https://library.sogang.ac.kr/htmlmanager/service/822"},# 외부링크 달려있음
            {"이름": "연구가이드 학과/주제별 자연과학", "URL": "https://library.sogang.ac.kr/htmlmanager/service/829"},# 외부링크 달려있음
            {"이름": "연구가이드 학과/주제별 공학", "URL": "https://library.sogang.ac.kr/htmlmanager/service/825"},# 외부링크 달려있음
            {"이름": "연구가이드 학과/주제별 법학", "URL": "https://library.sogang.ac.kr/htmlmanager/service/826"},# 메일주소 있음
            {"이름": "연구가이드 학과/주제별 통계", "URL": "https://library.sogang.ac.kr/htmlmanager/service/3900021"}, # 외부링크 달려있음
            {"이름": "연구가이드 논문작성 및 학술정보지원센터 논문작성법", "URL": "https://library.sogang.ac.kr/htmlmanager/service/1154421"}, # 외부링크 달려있음
            {"이름": "연구가이드 논문작성 및 학술정보지원센터 로욜라지식발전소", "URL": "https://library.sogang.ac.kr/htmlmanager/service/1971621"}, # 소분류의 소분류인데 또 소분류가 달려있음.
            {"이름": "연구가이드 논문작성 및 학술정보지원센터 연구윤리", "URL": "https://library.sogang.ac.kr/htmlmanager/service/3896421"}, # 외부링크 달려있음

            {"이름": "핵심 전자자료 가이드", "URL": "https://library.sogang.ac.kr/htmlmanager/service/5"},
            {"이름": "표절예방시스템 Turnitin", "URL": "https://library.sogang.ac.kr/htmlmanager/service/7"},

            {"이름": "참고문헌관리 EndNote/RefWorks", "URL": "https://library.sogang.ac.kr/htmlmanager/service/2163621"},#
            {"이름": "참고문헌관리 EndNote/RefWorks EndNote", "URL": "https://library.sogang.ac.kr/htmlmanager/service/2163621"},# 소소소
            {"이름": "참고문헌관리 EndNote/RefWorks RefWorks", "URL": "https://library.sogang.ac.kr/htmlmanager/service/8"}, # 소소소

            {"이름": "학위논문제출", "URL": "https://library.sogang.ac.kr/htmlmanager/service/9"},

            {"이름": "등재 학술지 리스트", "URL": "https://library.sogang.ac.kr/htmlmanager/service/501"},# 외부링크 달려있음
            
            {"이름": "OA출판 및 APC(논문출판비용) 지원", "URL": "https://library.sogang.ac.kr/htmlmanager/service/5618421"}, #
            {"이름": "OA출판 및 APC(논문출판비용) 지원 OA 출판 및 APC 지원 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/5618421"}, # 소소소
            {"이름": "OA출판 및 APC(논문출판비용) 지원 OA 플랫폼 및 정책 정보", "URL": "https://library.sogang.ac.kr/htmlmanager/service/5653221"}# 소소소
        ]
    },
    {
        "대분류": "도서관 이용",
        "중분류": "자료 이용",
        "소분류": [
            {"이름": "자료 대출 반납 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/10"},#
            {"이름": "자료 대출 반납 안내 대출 권수 및 기간", "URL": "https://library.sogang.ac.kr/htmlmanager/service/10"},
            {"이름": "자료 대출 반납 안내 대출/연장/예약", "URL": "https://library.sogang.ac.kr/htmlmanager/service/196"}, # 소소소
            {"이름": "자료 대출 반납 안내 반납/연체/변상", "URL": "https://library.sogang.ac.kr/htmlmanager/service/198"},# 소소소

            {"이름": "전자자료 이용 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/13"},#
            {"이름": "전자자료 이용 안내 이용 TIP", "URL": "https://library.sogang.ac.kr/htmlmanager/service/13"},
            {"이름": "전자자료 이용 안내 전자자료 공정 이용 ", "URL": "https://library.sogang.ac.kr/htmlmanager/service/203"},
            {"이름": "전자자료 이용 안내 교외접속", "URL": "https://library.sogang.ac.kr/htmlmanager/service/204"},

            {"이름": "희망자료 신청", "URL": "https://library.sogang.ac.kr/htmlmanager/service/16"},#
            {"이름": "희망자료 신청 이용안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/16"},# 소소소
            {"이름": "희망자료 신청 신청", "URL": "https://library.sogang.ac.kr/purchaserequest/write"},# 외부링크 달려있음
            
            {"이름": "타도서관 자료 대출", "URL": "https://library.sogang.ac.kr/htmlmanager/service/17"},
            {"이름": "타도서관 자료 복사", "URL": "https://library.sogang.ac.kr/htmlmanager/service/18"},
            {"이름": "서가에 없는 자료", "URL": "https://library.sogang.ac.kr/htmlmanager/service/19"}
        ]
    },
    {
        "대분류": "도서관 이용",
        "중분류": "시설 이용",
        "소분류": [
            {"이름": "개관시간", "URL": "https://library.sogang.ac.kr/htmlmanager/service/20"},

            {"이름": "일반열람실 및 스터디룸 이용안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/21"},#
            {"이름": "일반열람실 및 스터디룸 이용안내 일반열람실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/21"},
            {"이름": "일반열람실 및 스터디룸 이용안내 스터디룸 1~4 (3관 5층)", "URL": "https://library.sogang.ac.kr/htmlmanager/service/187"},
            {"이름": "일반열람실 및 스터디룸 이용안내 스터디룸 5~8 (1관 1층)", "URL": "https://library.sogang.ac.kr/htmlmanager/service/5522421"},

            {"이름": "전시 및 행사 공간 이용안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/26"},#
            {"이름": "전시 및 행사 공간 이용안내 로욜라 이주연 갤러리 이용 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/26"},# 신청서 링크
            {"이름": "전시 및 행사 공간 이용안내 신숙원 U-Dream Hall 이용 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/82"},# 신청서 링크

            {"이름": "라파엘 라이브 스튜디오 이용 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/4179621"},#
            {"이름": "라파엘 라이브 스튜디오 이용 안내 촬영 스튜디오", "URL": "https://library.sogang.ac.kr/htmlmanager/service/4179621"}, # 신청서 링크
            {"이름": "라파엘 라이브 스튜디오 이용 안내 편집실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/4189221"}, 
            
            {"이름": "캐럴 이용 신청", "URL": "https://library.sogang.ac.kr/htmlmanager/service/28"},
            {"이름": "복사 출력 스캔 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/29"},
            {"이름": "무선랜 이용 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/30"},
            {"이름": "모바일 이용증 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/31"},
            {"이름": "타도서관 이용 신청", "URL": "https://library.sogang.ac.kr/htmlmanager/service/32"}
        ]
    },
    {
        "대분류": "도서관 이용",
        "중분류": "이용자별 이용안내",
        "소분류": [
            {"이름": "학생", "URL": "https://library.sogang.ac.kr/htmlmanager/service/33"},
            {"이름": "교직원", "URL": "https://library.sogang.ac.kr/htmlmanager/service/34"},
            {"이름": "졸업생", "URL": "https://library.sogang.ac.kr/htmlmanager/service/35"},
            {"이름": "도서관회원", "URL": "https://library.sogang.ac.kr/htmlmanager/service/36"},
            {"이름": "협정기관", "URL": "https://library.sogang.ac.kr/htmlmanager/service/37"},
            {"이름": "장애인", "URL": "https://library.sogang.ac.kr/htmlmanager/service/38"},
            {"이름": "기타", "URL": "https://library.sogang.ac.kr/htmlmanager/service/39"}
        ]
    },
    {
        "대분류": "도서관 소개",
        "중분류": "로욜라 도서관",
        "소분류": [
            {"이름": "연혁", "URL": "https://library.sogang.ac.kr/htmlmanager/service/40"},
            {"이름": "자료현황", "URL": "https://library.sogang.ac.kr/htmlmanager/service/41"},
            {"이름": "시설현황", "URL": "https://library.sogang.ac.kr/htmlmanager/service/42"},
            {"이름": "조직 및 업무별 연락처", "URL": "https://library.sogang.ac.kr/htmlmanager/service/43"},
            {"이름": "규정", "URL": "https://library.sogang.ac.kr/htmlmanager/service/44"},
            {"이름": "비전", "URL": "https://library.sogang.ac.kr/htmlmanager/service/46"},
            
            {"이름": "오시는 길/층별 안내", "URL": "https://library.sogang.ac.kr/htmlmanager/service/83"},#
            {"이름": "오시는 길/층별 안내 도서관위치", "URL": "https://library.sogang.ac.kr/htmlmanager/service/83"},
            {"이름": "오시는 길/층별 안내 로욜라 1관", "URL": "https://library.sogang.ac.kr/htmlmanager/service/84"},
            {"이름": "오시는 길/층별 안내 로욜라 2관", "URL": "https://library.sogang.ac.kr/htmlmanager/service/85"},
            {"이름": "오시는 길/층별 안내 로욜라 3관", "URL": "https://library.sogang.ac.kr/htmlmanager/service/86"},
            {"이름": "오시는 길/층별 안내 X관(법학전문도서관)", "URL": "https://library.sogang.ac.kr/htmlmanager/service/91"},
            {"이름": "오시는 길/층별 안내 PA관 일반열람실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/89"},
            {"이름": "오시는 길/층별 안내 K관 일반열람실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/88"},
            {"이름": "오시는 길/층별 안내 X관 일반열람실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/90"},
            {"이름": "오시는 길/층별 안내 J관 일반열람실", "URL": "https://library.sogang.ac.kr/htmlmanager/service/87"}
        ]
    },
    {
        "대분류": "도서관 소개",
        "중분류": "분관안내",
        "소분류": [
            {"이름": "법학전문도서", "URL": "https://library.sogang.ac.kr/law"}
    
        ]
    },
    
    {
        "대분류": "도서관 소개",
        "중분류": "도서관 기부",
        "소분류": [
            {"이름": "자료기증", "URL": "https://library.sogang.ac.kr/htmlmanager/service/49"}
        
        ]
    }
]

runner = CrawlerRunner(url_data)
runner.run()