import google.generativeai as genai
import os
from .config import *
from .functions import helper_functions

print("Reading key")
key = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=key)

model_1_5_flash = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTIONS,
    tools=helper_functions,
)

model_1_5_pro = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTIONS,
    tools=helper_functions,
)

model_1_0_pro = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    system_instruction=SYSTEM_INSTRUCTIONS,
    tools=helper_functions,
)

summarizer_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You will be given a conversation between a user and an Ai model, your job is to return a brief title of that conversation. Return only the title"
)

model_dict = {
    "Gemini-1.5-Flash": model_1_5_flash,
    "Gemini-1.5-Pro": model_1_5_pro,
    # "Gemini-1.0-Pro": model_1_0_pro,
}

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
async def get_model(name : str) -> genai.GenerativeModel:
    return model_dict[name]

def get_available_models() -> list[str] :
    return list(model_dict.keys())  


def get_summarizer_model() -> genai.GenerativeModel:
    return summarizer_model