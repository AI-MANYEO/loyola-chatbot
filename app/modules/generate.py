from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger
from app.modules.search import search_library
<<<<<<< HEAD

logger = setup_logger(name="generate")
load_dotenv()

openai_key = os.environ.get("OPENAI_SECRET_KEY")
client = OpenAI(api_key=openai_key)
GPT_MODEL = "gpt-4"
=======
logger=setup_logger(name="generate")
load_dotenv()

openai_key=os.environ.get("OPENAI_SECRET_KEY")
client=OpenAI(api_key=openai_key)
GPT_MODEL="gpt-4"
>>>>>>> origin/sorin

def generate_response(query):
    results = search_library(query, top_k=1)

<<<<<<< HEAD
    # ✅ `results`가 None이거나 빈 리스트이면 예외 처리
    if not results or len(results) == 0:
        return "관련된 정보를 찾지 못했습니다."

    # ✅ `results`가 리스트 안에 리스트 형태일 경우 평탄화
    if isinstance(results[0], list):
        results = [item for sublist in results for item in sublist]  # 리스트 평탄화

    # ✅ `results`를 반복문에서 안전하게 처리
    context_text = "\n\n".join([
        f"출처: {r.get('title', '제목 없음')} ({r.get('category', '카테고리 없음')} > {r.get('subcategory', '서브카테고리 없음')})\n내용: {r.get('content', '정보 없음')}"
        for r in results if isinstance(r, dict)  # ✅ `r`이 딕셔너리인지 확인
    ])

    messages = [
        {"role": "system", "content": "당신은 서강대학교 도서관 이용을 돕는 친절한 챗봇입니다. 주어진 정보를 바탕으로 질문에 대한 정확한 답변을 제공하세요. 담당 부서와 연락처 정보도 함께 포함해야 합니다. 정확하지 않은 정보는 제공하지 마세요."},
=======

    if not results or len(results) == 0:
        return "관련된 정보를 찾지 못했습니다."

    if isinstance(results[0], list):
        results = results[0]

    context_text = "\n\n".join([
        f"출처: {r.get('title', '제목 없음')} ({r.get('category', '카테고리 없음')} > {r.get('subcategory', '서브카테고리 없음')})\n내용: {r.get('content', '정보 없음')}"
        for r in results
    ])


    messages = [
        {"role": "system", "content": "당신은 서강대학교 도서관 이용을 돕는 친절한 챗봇입니다. 주어진 정보를 바탕으로 질문에 대한 정확한 답변을 제공하세요. 담당 부서와 연락처 정보도 함께 포함해야 합니다."},
>>>>>>> origin/sorin
        {"role": "user", "content": f"질문: {query}\n관련 정보:\n{context_text}"}
    ]

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,  
            messages=messages,
            max_tokens=1000,
<<<<<<< HEAD
        )
        response_message = response.choices[0].message.content
=======
            #temperature=0.5,
        )
        response_message=response.choices[0].message.content
>>>>>>> origin/sorin
        return response_message
    except Exception as e:
        return f"답변 생성 중 오류가 발생했습니다: {e}"

<<<<<<< HEAD
#if __name__ == "__main__":
#    query = input("질문을 입력하세요: ")
#    response = generate_response(query)
#    print("AI 응답:", response)
=======
   

# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     response = generate_response(query)
#     print("AI 응답:", response)
>>>>>>> origin/sorin
