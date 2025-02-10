# loyola_chatbot
2025 winter 서강대학교 탐구공동체 프로젝트
---

## 📌 프로젝트 소개
도서관 정보 제공 및 부서 연결을 위한 객체 지향 인공지능 챗봇 프로젝트입니다.
모듈화된 AI 기술을 활용하여 질문에 답변을 제공하거나 관련 부서로 연결해주는 서비스를 개발합니다.

---

## 📂 프로젝트 디렉토리 구조

```plaintext
loyola-chatbot
├── README.md  # 프로젝트 개요 및 실행 방법
├── app
│   ├── api
│   ├── interfaces
│   ├── modules
│   │   ├── crawling_detail.py  # 상세 페이지 크롤러
│   │   ├── crawling_menu.py  # 메뉴 크롤러
│   │   ├── generate.py  # GPT 응답 생성
│   │   ├── save.py  # 크롤링 데이터를 크로마DB에 저장
│   │   ├── search.py  # 크로마DB에서 검색 수행
│   │   ├── ui.py  # Gradio 기반 UI
│   └── utils
│       ├── config.py  # 환경설정 파일
│       ├── logger.py  # 로깅 설정
├── app.log  # 로그 파일
├── check_db.py  # 크로마DB 데이터 확인 스크립트
├── database
│   ├── chroma_manager.py  # 크로마DB 설정 및 관리
│   └── raw
│       ├── detail_data.json  # 크롤링한 상세 페이지 데이터
│       └── menu_data.json  # 크롤링한 메뉴 데이터
├── main.py  # 챗봇 실행 엔트리포인트
├── requirements.txt  # Python 패키지 목록
└── static
    ├── fonts      
```
---
## 🚀 주요 기능

#### 1️⃣ 크롤링 (Crawling)
서강대학교 도서관 웹사이트에서 정보를 크롤링하여 JSON 파일로 저장합니다.
* 메뉴 크롤링 (crawling_menu.py): 도서관의 주요 메뉴 구조를 가져옴
* 상세 페이지 크롤링 (crawling_detail.py): 각 메뉴 항목의 상세 정보를 가져옴 (문의처 포함)

#### 2️⃣ 데이터 저장 (Save to ChromaDB)
* 크롤링한 데이터를 크로마DB에 저장 (save.py)
* 저장된 데이터는 벡터 임베딩을 사용하여 검색 가능

#### 3️⃣ 검색 (Search)
* 크로마DB에서 관련 정보를 검색 (search.py)
* 유사도가 높은 정보를 추출하여 응답 생성

#### 4️⃣ GPT 응답 생성 (Generate Response)
* 검색된 정보를 기반으로 GPT 모델 (gpt-4)을 이용해 답변 생성 (generate.py)

#### 5️⃣ 챗봇 UI (User Interface)
* Gradio를 활용한 챗봇 UI (ui.py)
* 사용자가 입력한 질문을 처리하고 결과를 표시

---

## 🚀 설치 및 실행 방법
#### 1. 프로젝트 클론
```bash
git clone https://github.com/AI-MANYEO/loyola-chatbot.git
cd loyola-chatbot
```

#### 2. 가상환경 활성화 및 라이브러리 설치
```bash
python -m venv venv
source ./venv/Scripts/activate # Windows
source ./venv/bin/activate # Mac/Linux
python --version
pip install -r requirements.txt
```

#### 3. .env 파일 설정
다음 환경 변수를 .env 파일에 추가합니다.
```plaintext
OPENAI_SECRET_KEY=your_openai_api_key
CHROMADB_HOST=your_chromadb_host
CHROMADB_PORT=your_chromadb_port
```

#### 4. 크롤링 실행
도서관 웹사이트에서 데이터를 수집하여 JSON 파일로 저장합니다.
```bash
python app/modules/crawling_menu.py # 메뉴 크롤링
python app/modules/crawling_detail.py # 상세 정보 크롤링
```

#### 5. 크로마DB에 데이터 저장
크롤링한 데이터를 크로마DB에 업로드합니다.
```bash
python app/modules/save.py
```

#### 6. 챗봇 실행
Gradio UI를 실행하여 챗봇을 사용할 수 있습니다.
```bash
python main.py
```
