from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.base_kb import main_menu_keyboard

from api.base import create_tg_user

from config import dp


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await check_user_state(message, state)
    
    initial_message = await message.answer("Добро пожаловать! Идет загрузка меню...")
    
    keyboard = main_menu_keyboard()
    await initial_message.edit_text(
        "Добро пожаловать! Пожалуйста, выберите действие:",
        reply_markup=keyboard
    )
    
    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
    }
    await create_tg_user(data)


def register_main_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])


async def check_user_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.reply("Вы начали новую операцию без завершения предыдущей. Ваш предыдущий процесс был сброшен.")
        await state.finish()  