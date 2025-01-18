from openai import OpenAI
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger

logger=setup_logger(name="generate")
load_dotenv()

openai_key=os.environ.get("OPENAI_SECRET_KEY")
client=OpenAI(api_key=openai_key)
GPT_MODEL="gpt-3.5-turbo"

'''
search.py에서 유사도 검색으로 찾은 데이터로 gpt가 답변 생성하는 것
'''
def generate_answer(query, similar_question, similar_answer):
    # messages = [
    #     {"role": "system", "content": "You are a helpful Sogagng University library chatbot.You must reply in Korean."},
    #     {"role": "user", "content": f"User Question: {query}"},
    #     {"role": "assistant", "content": f"Relevant FAQ Question: {similar_question}\nRelevant FAQ Answer: {similar_answer}"},
    #     {"role": "user", "content": "Can you provide a detailed and user-friendly answer based on this information? You must provide your answer in Korean."},
    # ]
    messages=[
        {"role": "system", "content": "You are a helpful Sogagng University library chatbot.You must reply in Korean."},
        {"role": "user", "content": f"User Question: {query}"},
        {"role": "assistant", "content": f"Relevant Information: {similar_question, similar_answer}"},
        {"role": "user", "content": "Can you provide a detailed and user-friendly answer based on this information? You must provide your answer in Korean."},
    ]

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,  
            messages=messages,
            max_tokens=1000,
            #temperature=0.7,
        )
        # response_dict=response.model_dump()
        # response_message = response_dict["choices"][0]["message"]["content"]
        response_message=response.choices[0].message.content
        return response_message
    except Exception as e:
        return f"답변 생성 중 오류가 발생했습니다: {e}"