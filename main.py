from app.utils.logger import setup_logger
# from app.modules.search import get_answer
from app.modules.save_chroma import load_data_to_chromadb
from app.modules.generate_chroma import generate_response
import pandas as pd

# def main():
#     print("도서관 챗봇에 오신 것을 환영합니다!")
#     print("질문을 입력해 주세요. 종료하려면 'exit'를 입력하세요.")
    
#     while True:
#         # Get user input
#         user_query = input("\n[사용자 질문] > ")
        
#         # Exit condition
#         if user_query.lower() == "exit":
#             print("챗봇을 종료합니다. 이용해 주셔서 감사합니다!")
#             break
        
#         # Get the answer
#         answer = get_answer(faq_data, user_query)
#         print(f"[챗봇 답변] > {answer}")

if __name__ == "__main__":
    #main()
    #load_data_to_chromadb()
    query=input("질문을 입력하세요: ")
    response=generate_response(query)
    print("챗봇 응답: ", response)