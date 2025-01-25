from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger
from app.modules.search import search_library

logger = setup_logger(name="generate")
load_dotenv()

openai_key=os.environ.get("OPENAI_SECRET_KEY")
client=OpenAI(api_key=openai_key)
GPT_MODEL="gpt-4"

# 담당 부서 정보
contact_info = "정보서비스팀의 참고서비스데스크(02-705-8195)"

def generate_response(query):
    results = search_library(query, top_k=1)


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
        {"role": "user", "content": f"질문: {query}\n관련 정보:\n{context_text}"}
    ]

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            max_tokens=1000,
            #temperature=0.5,
        )
        response_message = response.choices[0].message.content
        
        # 최종 응답에 담당 부서 정보 추가
        final_response = f"{response_message}\n\n추가 문의사항이 있으시면 {contact_info}로 연락해주세요."
        return final_response

    except Exception as e:
        logger.error(f"API 호출 오류: {e}")
        return f"답변 생성 중 오류가 발생했습니다: {e}"

# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     response = generate_response(query)
#     print("AI 응답:", response)