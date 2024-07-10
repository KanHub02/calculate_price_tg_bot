from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.base_kb import (
    main_menu_keyboard,
    utilities_menu_keyboard,
    manager_menu_keyboards,
    after_translation_course,
)

from api.base import create_tg_user

from config import bot, logger


async def send_welcome(message: types.Message, state: FSMContext):
    await check_user_state(message, state)

    initial_message = await message.answer("Добро пожаловать! Идет загрузка меню...")

    keyboard = main_menu_keyboard()
    await initial_message.edit_text(
        "Добро пожаловать! Пожалуйста, выберите действие:", reply_markup=keyboard
    )

    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
    }
    await create_tg_user(data)


async def handle_main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите опцию:",
        reply_markup=main_menu_keyboard(),
    )


async def handle_utilities_menu(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите опцию:",
        reply_markup=manager_menu_keyboards(),
    )


async def handle_exchange_rate_menu(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        text="Выберите опцию:",
        reply_markup=after_translation_course(),
    )


def register_main_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_callback_query_handler(
        handle_main_menu, lambda c: c.data == "main_menu"
    )
    dp.register_callback_query_handler(
        handle_utilities_menu, lambda c: c.data == "utilities"
    )
    dp.register_callback_query_handler(
        handle_exchange_rate_menu, lambda c: c.data == "exchange_rate"
    )


async def check_user_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.reply(
            "Вы начали новую операцию без завершения предыдущей. Ваш предыдущий процесс был сброшен."
        )
        await state.finish()
