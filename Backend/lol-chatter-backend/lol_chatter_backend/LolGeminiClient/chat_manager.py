from operator import itemgetter
import google.generativeai as genai
from lol_chatter_backend.Models.chat import ChatSession, ChatMessage
from langchain_core.language_models.chat_models import BaseChatModel
from lol_chatter_backend.LolGeminiClient.prompts import (
    contextualize_q_prompt,
    qa_prompt,
)
from lol_chatter_backend.LolGeminiClient.model_generation import create_model
from langchain_core.runnables import RunnableBranch
from lol_chatter_backend.LolGeminiClient.retriever import get_retriever
from langchain.schema import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage


class ChatManager:

    def __init__(self, model: BaseChatModel):
        self.model = model
        self.rephrase_llm = create_model("gemini-1.5-flash")
        retriever = get_retriever()
        self.retriever_chain = (
            contextualize_q_prompt | self.rephrase_llm | StrOutputParser()
        )

        self.chain = (
            {
                "context": RunnableBranch(
                    (lambda x: x["chat_history"], self.retriever_chain | StrOutputParser()),  # type: ignore
                    (lambda x: not x["chat_history"], itemgetter("input")),  # type: ignore
                    self.retriever_chain | StrOutputParser(),
                )
                | retriever,
                "input": itemgetter("input"),
                "chat_history": itemgetter("chat_history"),
            }
            | qa_prompt
            | model
            | StrOutputParser()
        )

    def process_history(self, history: list[ChatMessage] = []):
        chats = []
        for msg in history:
            if msg.role == "user":
                chats.append(HumanMessage(content=msg.content))
            else:
                chats.append(AIMessage(content=msg.content))

        return chats

    def send_msg_streaming(self, user_msg: str, history: list[ChatMessage] = []):
        chats = self.process_history(history)

        return self.chain.astream({"input": user_msg, "chat_history": chats})

    def send_msg(self, user_msg: str, history: list[ChatMessage] = []):
        chats = self.process_history(history)
        return self.chain.invoke({"input": user_msg, "chat_history": chats})
