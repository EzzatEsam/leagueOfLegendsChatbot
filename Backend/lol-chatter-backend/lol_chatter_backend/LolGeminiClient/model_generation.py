import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

sefety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold(2),
    HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold(2),
    HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold(2),
    HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold(2),
}


def create_model(name: str) -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=name,
        max_retries=2,
        safety_settings=sefety_settings,
        # other params...
    )


summarizer_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You will be given a conversation between a user and an Ai model, your job is to return a brief title of that conversation. Return only the title",
)

model_dict = {
    "Gemini-1.5-Flash": create_model("gemini-1.5-flash"),
    "Gemini-1.5-Pro": create_model("gemini-1.5-pro"),
    "Gemini-1.0-Pro": create_model("gemini-1.0-pro"),
}

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)


async def get_model(name: str) -> BaseChatModel:
    return model_dict[name]


def get_available_models() -> list[str]:
    return list(model_dict.keys())


def get_summarizer_model() -> genai.GenerativeModel:
    return summarizer_model
