from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger
from app.modules.search_chroma import search_library
logger=setup_logger(name="generate")
load_dotenv()

openai_key=os.environ.get("OPENAI_SECRET_KEY")
client=OpenAI(api_key=openai_key)
GPT_MODEL="gpt-3.5-turbo"

def generate_response(query):
    results = search_library(query)


    if not results or len(results) == 0:
        return "관련된 정보를 찾지 못했습니다."

    best_match = results[0] 

    messages=[
            {"role": "system", "content": "당신은 도서관 이용을 도와주는 챗봇입니다. 관련 정보를 토대로, 주어진 사용자의 질문에 알맞은 응답을 생성해주세요. 답변은 친절하고 명확해야합니다. 추가 문의사항을 처리할 수 있는 담당 부서와 연락처 정보를 함께 제공해야합니다."},
            {"role": "user", "content": f"질문: {query}\n관련 정보: {best_match.get('content', '정보 없음')}"},
    ]

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,  
            messages=messages,
            max_tokens=1000,
            #temperature=0.7,
        )
        response_message=response.choices[0].message.content
        return response_message
    except Exception as e:
        return f"답변 생성 중 오류가 발생했습니다: {e}"

   

# if __name__ == "__main__":
#     query = input("질문을 입력하세요: ")
#     response = generate_response(query)
#     print("AI 응답:", response)