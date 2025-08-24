import nest_asyncio
nest_asyncio.apply()
import logging
import aiosqlite
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data import quiz_data

logging.basicConfig(level=logging.INFO)

DB_NAME = 'quiz_bot.db'

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(answer_options):
        callback_data = f"{'right_answer' if option == right_answer else 'wrong_answer'}:{index}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data)
        )

    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id,new_score)
    await get_question(message, user_id)

async def get_quiz_index(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_user_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM users WHERE user_id=?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_user_score(user_id, new_score):
  async with aiosqlite.connect(DB_NAME) as db:
    await db.execute('INSERT INTO users(user_id, score) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET score=excluded.score', (user_id, new_score))
    await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')
        await db.commit()