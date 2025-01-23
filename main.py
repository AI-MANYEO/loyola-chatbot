from app.utils.logger import setup_logger
# from app.modules.search import get_answer
from app.modules.save_chroma import load_data_to_chromadb
from app.modules.generate_chroma import generate_response
import pandas as pd
import gradio as gr

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

def chatbot_interface(query):
    response=generate_response(query)
    return response

interface = gr.Interface(
    fn=chatbot_interface,               # Gradio가 호출할 함수
    inputs=gr.Textbox(label="질문을 입력하세요"),  # 사용자 입력
    outputs=gr.Textbox(label="챗봇 응답")         # 챗봇 출력
)

# if __name__ == "__main__":
#     #main()
#     #load_data_to_chromadb()
#     query=input("질문을 입력하세요: ")
#     response=generate_response(query)
#     print("챗봇 응답: ", response)

if __name__ == "__main__":
    # Gradio 인터페이스 실행
    interface.launch()

# if __name__ == "__main__":
#     load_data_to_chromadb()