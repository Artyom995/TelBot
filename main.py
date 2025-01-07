import asyncio
import logging
import sqlite3

from database import create_table
from bot import dp, bot
import handlers

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
 

async def main():

    await create_table()
    # Запускаем поллинг для получения обновлений
    await dp.start_polling(bot)
       
if __name__ == "__main__":
    asyncio.run(main())