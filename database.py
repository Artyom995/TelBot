import sqlite3

# функция для создания базы данных и таблицы
def create_database():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_answers (
        user_id INTEGER,
        answer TEXT
    )
    ''')

    conn.commit()
    conn.close()

#берем в базу данных
def save_user_answer(user_id, answer):
    # Создаем подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        answer TEXT
    )
    ''')

    # Вставляем ответ пользователя
    cursor.execute('''
    INSERT INTO user_answers (user_id, answer) VALUES (?, ?)
    ''', (user_id, answer))

    conn.commit()
    conn.close()

    
#берем из базы данных
def get_user_answer(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Получаем все ответы пользователя
    cursor.execute('SELECT answer FROM user_answers WHERE user_id = ?', (user_id,))
    answers = cursor.fetchall()  # Получаем все ответы
    
    conn.close()
    
    # Возвращаем количество правильных ответов
    return len(answers)  # Возвращаем длину списка ответов

#очистить таблицу 
def clear_user_answers():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Очищаем таблицу user_answers
    cursor.execute('DELETE FROM user_answers')

    conn.commit()
    conn.close()
