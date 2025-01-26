from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import pygsheets

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
SPREADSHEET_NAME = "Название таблицы"

class GoogleSheets:
    def __init__(self):
        self.gc = pygsheets.authorize()
        self.sh = self.gc.open(SPREADSHEET_NAME)
        self.wks = self.sh.sheet1

    def read_data(self):
        try:
            return self.wks.get_all_values()
        except Exception as e:
            print(f"Ошибка чтения: {e}")
            return None

    def write_data(self, data):
        try:
            self.wks.append_table([data])
            return True
        except Exception as e:
            print(f"Ошибка записи: {e}")
            return False

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
sheets = GoogleSheets()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для работы с таблицей.\n"
        "/read - прочитать\n"
        "/write текст - записать"
    )

@dp.message(Command("read"))
async def cmd_read(message: types.Message):
    data = sheets.read_data()
    if data:
        response = "Данные:\n" + "\n".join([", ".join(row) for row in data])
        await message.answer(response[:4000])
    else:
        await message.answer("Ошибка чтения")

@dp.message(Command("write"))
async def cmd_write(message: types.Message):
    text = message.text.replace('/write', '').strip()
    if text:
        if sheets.write_data(text):
            await message.answer("Записано")
        else:
            await message.answer("Ошибка записи")
    else:
        await message.answer("Укажите текст")

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
        print("Бот остановлен")
        sys.exit()