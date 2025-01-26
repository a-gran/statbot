from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import logging
from env.credentials import key
import os
import sys
import pygsheets

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=key)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я тестовый бот.\n"
        "Доступные команды:\n"
        "/help - показать помощь"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Список команд:\n"
        "/start - начать работу с ботом\n"
        "/help - показать это сообщение"
    )

@dp.message(F.text)
async def handle_text(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("Красивое фото!")

@dp.message(F.sticker)
async def handle_sticker(message: types.Message):
    await message.answer("👍")

async def main():
    try:
        print("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        print("Бот остановлен")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выключение бота")
        sys.exit()