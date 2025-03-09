"""
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_ai_response(user_message):
    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content

# Пример вызова функции
print(get_ai_response("Какие услуги у вас есть?"))
"""
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from config.config import TOKEN
from bot.ai_assistant import get_ai_response  # Подключаем OpenAI API

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    response = get_ai_response("Привет! Какие услуги у вас есть?")
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
