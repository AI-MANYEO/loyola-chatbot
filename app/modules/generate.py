from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger
from app.modules.search import search_library

logger = setup_logger(name="generate")
load_dotenv()

openai_key = os.environ.get("OPENAI_SECRET_KEY")
client = OpenAI(api_key=openai_key)
GPT_MODEL = "gpt-4"

# 담당 부서 정보
contact_info = "정보서비스팀의 참고서비스데스크(02-705-8195)"

def generate_response(query):
    results = search_library(query)

    if not results or len(results) == 0:
        return f"관련된 정보를 찾지 못했습니다. 추가 도움이 필요하면 {contact_info}로 연락해주세요."

    # 상위 3개의 검색 결과를 활용
    top_results = results[:3]
    combined_results = "\n".join([f"[{i+1}] {res.get('content', '정보 없음')}" for i, res in enumerate(top_results)])

    messages = [
        {"role": "system", "content": "당신은 도서관 이용을 도와주는 챗봇입니다. 관련 정보를 토대로, 주어진 사용자의 질문에 알맞은 응답을 생성해주세요. 답변은 친절하고 명확해야 합니다. 추가 문의사항을 처리할 수 있는 담당 부서와 연락처 정보를 함께 제공해야 합니다."},
        {"role": "user", "content": f"질문: {query}\n관련 검색 결과:\n{combined_results}"},
    ]

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            max_tokens=1000,
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