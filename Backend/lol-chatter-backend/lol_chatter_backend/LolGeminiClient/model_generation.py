import google.generativeai as genai
import os

print("Reading key")
key = os.environ.get("GOOGLE_API_KEY")


model = genai.GenerativeModel(model_name="gemini-1.5-flash")

async def get_model() :
    return model