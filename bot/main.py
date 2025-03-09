import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config.config import TOKEN
from bot.ai_assistant import get_ai_response

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я ваш виртуальный ассистент. Как могу помочь?")

# Обработчик всех сообщений (общение через OpenAI Assistants API)
@dp.message()
async def chat_with_ai(message: Message):
    # Показываем статус "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    # Отправляем сообщение в OpenAI
    response = get_ai_response(message.from_user.id, message.text)
    # Отвечаем пользователю
    await message.answer(response)

async def main():
    print("✅ Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
