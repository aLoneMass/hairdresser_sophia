import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

openai_client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORG_ID
    )

def get_ai_response(user_message):
    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content
