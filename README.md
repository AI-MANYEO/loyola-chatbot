# loyola_chatbot
2025 winter 탐구 공동체 프로젝트

---

## 📌 프로젝트 소개
도서관 정보 제공 및 부서 연결을 위한 객체 지향 인공지능 챗봇 프로젝트입니다.
모듈화된 AI 기술을 활용하여 질문에 답변을 제공하거나 관련 부서로 연결해주는 서비스를 개발합니다.

---

## 📂 프로젝트 디렉토리 구조

```plaintext
chatbot
├── app                       # 애플리케이션 주요 모듈
│   ├── modules               # 주요 기능별 모듈(NLP, 크롤링, 검색 등)
│       ├── crawling_detail.py
│       ├── generate.py
│       ├── save.py
│       └── search.py
│   ├── interfaces            # 사용자 인터페이스 모듈
│       ├── ui.py
│   ├── utils                 # 공통 유틸리티 함수
│       ├── ⚙️ config.py        
│       └── 🛠️ logger.py
├── database                  # 크롤링 데이터 저장
│   ├── raw
│       └── detail_data.json
│   └── chroma_manager.py
└── main.py                   # 프로젝트 실행 파일           
```

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
source ./venv/Scripts/activate #Windows용
source ./venv/bin/activate #Mac용
python --version
pip install -r requirements.txt
```

#### 3. 메인 파일 실행
```bash
python main.py
```
