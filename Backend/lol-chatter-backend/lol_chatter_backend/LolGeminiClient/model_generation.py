import google.generativeai as genai
import os
from .config import *
from .functions import helper_functions

print("Reading key")
key = os.environ.get("GOOGLE_API_KEY")


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTIONS,
    tools=helper_functions,
)


async def get_model():

    return model
