import sqlite3
import aiosqlite
from config import DB_NAME


async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем SQL-запрос к базе данных для создания таблицы с новым столбцом 'answer'
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
                                user_id INTEGER PRIMARY KEY, 
                                question_index INTEGER, 
                                answer INTEGER
                            )''')
        
        # Сохраняем изменения
        await db.commit()


# Функция для добавления в базу нового пользователя и увеличения значения question_index на единицу
async def update_quiz_index(user_id, index, answer):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, answer) VALUES (?, ?, ?)', (user_id, index, answer))
        # Сохраняем изменения
        await db.commit()


#  функция, которая получит текущее значение question_index в базе данных для заданного пользователя.       
async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            

 #функция добавления в таблицу question_index       
async def update_question_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET question_index = ? WHERE user_id = ?', (index, user_id))
        await db.commit()


 #функция добавления в таблицу answer       
async def update_answer(user_id, answer):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET answer = ? WHERE user_id = ?', (answer, user_id))
        await db.commit()


#  функция, которая получит текущее значение answer в базе данных для заданного пользователя.      
async def get_quiz_answer(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT answer FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
