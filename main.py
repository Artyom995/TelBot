import nest_asyncio
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

nest_asyncio.apply()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '8091370425:AAG_15I-vMYfXZhhl5p4EoW0XngC8k0YSoI'


# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Логика обработки команды /start
    await message.answer("Привет! Я бот для проведения квиза. Введите /quiz, чтобы начать.")

# Хэндлер на команду /quiz
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Логика начала квиза
    await message.answer("Давайте начнем квиз! Первый вопрос: ...")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())