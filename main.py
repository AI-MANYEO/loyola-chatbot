from app.utils.logger import setup_logger
from app.modules.generate import generate_response
from app.modules.ui import build_ui
import gradio as gr

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

