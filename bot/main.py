from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from config.config import TOKEN
from bot.ai_assistant import get_ai_response  # Подключаем OpenAI API

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    response = get_ai_response("Привет! Какие услуги у вас есть?")
    await message.answer(response)

# Обработчик обычных сообщений (позже можно улучшить)
@dp.message()
async def handle_message(message: Message):
    response = get_ai_response(message.text)
    await message.answer(response)

# Запуск бота  
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
