<<<<<<< HEAD
from app.modules.save import load_data_to_chromadb
from app.modules.save import reset_chromadb
=======
from app.utils.logger import setup_logger
>>>>>>> origin/sorin
from app.modules.generate import generate_response
from app.modules.ui import build_ui
import gradio as gr

<<<<<<< HEAD
def chatbot_interface(query):
    """챗봇 인터페이스 함수"""
    response = generate_response(query)
    return response

# Gradio UI 설정
interface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Textbox(label="질문을 입력하세요"),
    outputs=gr.Textbox(label="챗봇 응답")
)

if __name__ == "__main__":
    # ✅ 크로마DB 데이터 저장
    #reset_chromadb()  # 기존 데이터 초기화
    #load_data_to_chromadb()  # 데이터 저장

    # ✅ Gradio UI 실행
    ui = build_ui(generate_response)
    ui.launch()
=======
# 사용자가 입력한 질문에 대한 응답을 생성
def chatbot_interface(query, chat_history):
    response = generate_response(query)  # 응답 생성
    chat_history.append((query, response))  # 질문-응답 기록 추가
    return "", chat_history  # 입력창 초기화와 기록 반환

# 메인 함수
if __name__ == "__main__":
    # Gradio UI 생성 및 실행
    ui = build_ui(chatbot_interface)
    ui.launch()


>>>>>>> origin/sorin
