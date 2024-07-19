import google.generativeai as genai

from lol_chatter_backend.Models.chat import ChatMessage

class Summarizer:
    def __init__(self, model : genai.GenerativeModel):
        self.model = model

    def get_summarized_text(self, chats: list[ChatMessage]) -> str:
        history = ""
        
        for chat in chats:
            history += "Message 1: \n"
            history += f"role : {chat.role}\n"
            history += f"content : {chat.content}\n"
        
        result = self.model.generate_content(history)
        return result.text
    
