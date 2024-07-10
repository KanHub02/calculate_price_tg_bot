import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config
from api.feedback_usefull import send_feedback
from config import bot

logging.basicConfig(level=logging.INFO)


# Определение состояний машины состояний
class FeedbackForm(StatesGroup):
    feedback = State()


# Начало сбора отзыва
async def feedback_start(callback_query: types.CallbackQuery):
    await FeedbackForm.feedback.set()
    await bot.send_message(
        callback_query.from_user.id,
        "Пожалуйста, оставьте ваш отзыв по полезным статьям:",
    )


# Получение отзыва и отправка на сервер
async def feedback_received(message: types.Message, state: FSMContext):
    feedback = message.text
    user_id = message.from_user.id
    success = await send_feedback(user_id, feedback)
    if success:
        await message.reply("Спасибо за ваш отзыв!")
    else:
        await message.reply(
            "Произошла ошибка при отправке вашего отзыва. Пожалуйста, попробуйте позже."
        )
    await state.finish()


# Регистрация обработчиков
def register_feedback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        feedback_start, Text(equals="usefull_feedback"), state="*"
    )
    dp.register_message_handler(feedback_received, state=FeedbackForm.feedback)
