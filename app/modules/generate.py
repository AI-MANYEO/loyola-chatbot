from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger

logger=setup_logger(name="generate")
# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
openai_key = os.getenv("OPENAI_SECRET_KEY")

# API 키가 정상적으로 로드되었는지 확인
if not openai_key:
    raise ValueError("❌ OpenAI API Key가 설정되지 않았습니다! .env 파일을 확인하세요.")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=openai_key)
GPT_MODEL = "gpt-3.5-turbo"

'''
search.py에서 유사도 검색으로 찾은 데이터로 gpt가 답변 생성하는 것
'''
def generate_answer(query, similar_question, similar_answer):
    """
    Generates an AI-powered answer based on the query and the most relevant book data.
    """
    messages = [
        {"role": "system", "content": "당신은 서강대학교 도서관 챗봇입니다. 친절하고 정확한 정보를 제공하세요."},
        {"role": "user", "content": f"사용자 질문: {query}"},
        {"role": "assistant", "content": f"관련 도서 서명: {similar_question}\n소장 정보: {similar_answer}"},
        {"role": "user", "content": "위 정보를 바탕으로 사용자에게 상세하고 친절한 답변을 제공해주세요."}
    ]

    # **[디버깅 출력] GPT에게 전달되는 메시지 확인**
    print(f"\n[DEBUG] GPT 입력 데이터:")
    for msg in messages:
        print(f"[{msg['role'].upper()}] {msg['content']}\n")

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,  
            messages=messages,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"답변 생성 중 오류가 발생했습니다: {e}"
