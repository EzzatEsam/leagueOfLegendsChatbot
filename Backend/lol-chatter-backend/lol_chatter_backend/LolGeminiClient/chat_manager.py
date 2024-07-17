import google.generativeai as genai
from lol_chatter_backend.Models.chat import ChatSession, ChatMessage


class ChatManager:
    def __init__(self, model: genai.GenerativeModel, prev_messages: list[ChatMessage]):
        self.model = model

        history = [
            {"role": msg.role, "parts": [{"text": msg.content}]}
            for msg in prev_messages
        ]

        self.chat = self.model.start_chat(history=history, enable_automatic_function_calling=True)  # type: ignore

    def send_msg(self, msg: str):
        stream = self.chat.send_message(msg,
                                        # stream=True
                                        )
        return [stream]
