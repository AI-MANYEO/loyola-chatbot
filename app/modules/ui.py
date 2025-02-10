import gradio as gr

def build_ui(chatbot_interface):
    with gr.Blocks(css="""
        .send-button, .clear-button {
            padding: 12px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.2s;
        }
        .send-button {
            background-color: #861F1C;
            color: white;
        }
        .send-button:hover {
            background-color: #6A1718;
            transform: scale(1.05);
        }
        .clear-button {
            background-color: #808080;
            color: white;
        }
        .clear-button:hover {
            background-color: #5F5F5F;
            transform: scale(1.05);
        }
        .chat-container {
            height: 500px;  /* Increased height */
            overflow-y: auto;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #333;
        }
        .bot-message {
            background-color: #9C2A2A;  /* Lighter version of #861F1C */
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        .user-message, .user.svelte-u94xf4.message {
            background-color: rgba(134, 31, 28, 0.1);  /* 배경색 투명도 10% */
            border: 1px solid rgba(134, 31, 28, 0.2);  /* 테두리 색상, 두께, 투명도 설정 */
            border-radius: 10px;  /* 둥근 모서리 적용 */
            padding: 10px;
            color: white;  /* 글자 색상 */
            font-weight: bold;
        }
    """) as interface:

        chat_history = gr.State([])

        # Title with logo on the left (updated to use the new image)
        with gr.Row():
            gr.HTML("""
                <div class="header-title">
                    <img src="https://sogang.bookcosmos.com/logoImg/logo.gif" 
                        alt="Library Logo" 
                        style="cursor: pointer; width: 180px; height: auto;" 
                        onclick="location.reload();" />
                </div>
            """)

        # Chat history
        chatbot = gr.Chatbot(label="채팅 기록", elem_id="chat-container")

        # Input and buttons
        with gr.Row():
            user_input = gr.Textbox(
                placeholder="질문을 입력하세요",
                label="",
                lines=1,
                scale=8
            )
            send_btn = gr.Button("Send", elem_classes="send-button", scale=1)
            clear_btn = gr.Button("Clear", elem_classes="clear-button", scale=1)

        # Textbox에서 Enter 키로 메시지를 전송
        user_input.submit(
            chatbot_interface,
            inputs=[user_input, chat_history],
            outputs=[user_input, chatbot]
        )
        
        # Button events
        send_btn.click(
            chatbot_interface,
            inputs=[user_input, chat_history],
            outputs=[user_input, chatbot]
        )
        clear_btn.click(
            lambda: (None, []),
            inputs=None,
            outputs=[user_input, chatbot]
        )

    return interface