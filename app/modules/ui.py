import gradio as gr

def build_ui(chatbot_interface):
    interface = gr.Interface(
        fn=chatbot_interface,
        inputs=gr.Textbox(label="질문을 입력하세요"),
        outputs=gr.Textbox(label="챗봇 응답"),
        css="""
            .primary {
                background-color: #861F1C;  /* Submit 버튼 색상 */
                color: white;               /* 텍스트 색상 */
                border-radius: 8px;         /* 모서리 둥글게 */
                border: none;               /* 테두리 제거 */
            }
            .primary:hover {
                background-color: #6A1718;  /* 마우스 오버 시 색상 */
            }
        """
    )
    return interface
