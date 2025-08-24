import nest_asyncio
nest_asyncio.apply()
from aiogram import F,Router
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from function import new_quiz, get_user_score, get_quiz_index, update_user_score, update_quiz_index, get_question
from data import quiz_data
from aiogram.types import CallbackQuery
from initialization import router

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

@router.message(Command("help"))
async def cmd_start(message: types.Message):
  await message.answer("Команды бота:\n\start - начало работы бота \n\help - открыть помощь\n\quize - начать игру")
  
router = Router()

@router.callback_query(F.data.startswith(("right_answer", "wrong_answer")))
async def handle_answer(callback: CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    data_parts = callback.data.split(':')
    is_correct = data_parts[0] == "right_answer"
    selected_index = int(data_parts[1])

    current_question_index = await get_quiz_index(callback.from_user.id)
    selected_option = quiz_data[current_question_index]['options'][selected_index]

    await callback.message.answer(f"{selected_option}")
    
    current_score = await get_user_score(callback.from_user.id)

    if is_correct:
        await callback.message.answer("Верно!")
        current_score += 1
        await update_user_score(callback.from_user.id, current_score)
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
        )

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Ваш итоговый счет: {current_score}")
        