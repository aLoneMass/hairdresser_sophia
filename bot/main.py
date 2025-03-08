import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.config import TOKEN

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Я твой Telegram-бот 🤖")

# Обработчик команды /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Вот что я умею:\n/start - Приветствие\n/help - Список команд")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
