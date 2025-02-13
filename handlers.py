import sqlite3
from aiogram import  types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from function import new_quiz, get_question 
from config import quiz_data
from database import get_quiz_answer, update_question_index, update_answer, update_quiz_index, get_quiz_index


from bot import dp

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id    
    # Сброс данных о правильных ответах для нового квиза
    # Логика обработки команды /start
    # await message.answer("Привет! Я бот для проведения квиза. Введите /quiz, чтобы начать.")
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())
    # Запускаем новый квиз
    await new_quiz(message)

#Функция правильного ответа
@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    # Отправляем в чат сообщение, что ответ верный
    await callback.message.answer("Верно!")
    user_id = callback.from_user.id
    # обновляем таблицу ответов
    correct_answer = await get_quiz_answer(callback.from_user.id)
    # Преобразуем correct_answer в целое число, если это строка
    if isinstance(correct_answer, str):
        correct_answer = int(correct_answer)  # Преобразование в целое число

    correct_answer += 1  # Увеличиваем количество правильных ответов
    await update_answer(user_id, correct_answer)
    # Перезаписываем ответ в базе данных
    current_question_index += 1
    await update_question_index(user_id, current_question_index)
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Посмотреть результаты"))
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, user_id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!", reply_markup=builder.as_markup(resize_keyboard=True))



# Функция для обработки неправильного ответа
@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    # Редактируем текущее сообщение, чтобы убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    # Получаем индекс правильного ответа
    correct_option = quiz_data[current_question_index]['correct_option']
    # Отправляем сообщение об ошибке с указанием верного ответа
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_question_index(callback.from_user.id, current_question_index)
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Посмотреть результаты"))
    # Проверяем, достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Посмотреть результаты")
@dp.message(Command("results"))
async def cmd_results(message: types.Message):
    user_id = message.from_user.id
    
    # Получаем количество правильных ответов из базы данных
    correct_answers_count = await  get_quiz_answer(user_id)  # Используем функцию для получения количества ответов
    
    # Если пользователь не имеет сохраненных ответов, correct_answers_count будет None
    if correct_answers_count is None:
        correct_answers_count = 0  # Если ответов нет, то 0

    # Создаем клавиатуру с кнопкой "Повторить"
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Повторить"))
    
    # Отправляем новое сообщение с результатами
    await message.answer(f"Результаты вашего квиза: {correct_answers_count} из {len(quiz_data)}", reply_markup=builder.as_markup(resize_keyboard=True))

        
@dp.message(F.text == "Повторить")
async def cmd_repeat(message: types.Message):
    user_id = message.from_user.id
    # Сброс данных о правильных ответах для нового квиза
    await update_quiz_index(user_id, 0, 0)
    # Вызываем команду /start
    await cmd_quiz(message)