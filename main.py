from app.modules.save import load_data_to_chromadb
from app.modules.save import reset_chromadb
from app.modules.generate import generate_response
from app.modules.ui import build_ui
import gradio as gr

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
