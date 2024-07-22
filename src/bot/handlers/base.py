from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, bold, escape_md
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from keyboards.base_kb import (
    main_menu_keyboard,
    utilities_menu_keyboard,
    manager_menu_keyboards,
    after_translation_course,
    manager_menu_keyboards,
    single_menu_button
)

import aiohttp
from api.base import create_tg_user, get_manager_ids

from config import bot, logger, API_TOKEN


async def send_welcome(message: types.Message, state: FSMContext):
    await check_user_state(message, state)

    initial_message = await message.answer(
        text(bold("Добро пожаловать! Идет загрузка меню...")), parse_mode="Markdown"
    )

    keyboard = main_menu_keyboard()
    await initial_message.edit_text(
        text(
            bold("Добро пожаловать в UNCLE MAO 👹\n")
            + "\n"
            + "Выберите действие, чтобы продолжить"
        ),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
    }
    await create_tg_user(data)


async def handle_main_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Вы в главном меню",
        reply_markup=main_menu_keyboard(),
    )


async def handle_utilities_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите действие, чтобы продолжить",
        reply_markup=utilities_menu_keyboard(),
    )


async def handle_exchange_rate_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите действие, чтобы продолжить",
        reply_markup=after_translation_course(),
    )


async def handle_manage_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите действие, чтобы продолжить",
        reply_markup=manager_menu_keyboards(),
    )

async def send_user_request_to_manager(callback_query: types.CallbackQuery):
    managers_ids = await get_manager_ids()
    user_id = callback_query.from_user.id
    user_full_name = callback_query.from_user.full_name
    user_usernname =  callback_query.from_user.username
    message = (
        f"🚨 <b>Запрос на поддержку</b> 🚨\n\n"
        f"<b>Пользователь:</b> {user_full_name} (ID: {user_id}) (USERNAME: {user_usernname})\n"
        f"<b>Сообщение:</b> Пользователь отправил запрос на поддержку.\n\n"
        f"Пожалуйста, свяжитесь с пользователем как можно скорее."
    )
    await bot.send_message(callback_query.message.from_user.id, text="Вы отправили ваши контакты менеджеру, в скором времени с вами свяжутся!", reply_markup=single_menu_button())
    async with aiohttp.ClientSession() as session:
        for manager in managers_ids:
            chat_id = manager.get("tg_id")
            if chat_id:
                url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=HTML"
                async with session.get(url) as response:
                    if response.status == 200:
                        print(f"Сообщение успешно отправлено менеджеру с ID {chat_id}")
                    else:
                        print(f"Не удалось отправить сообщение менеджеру с ID {chat_id}, статус: {response.status}")

async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu")
    keyboard.add(button)
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await callback_query.message.edit_text(
        "Вы отменили текущий процесс 😕", reply_markup=keyboard
    )


async def check_user_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.reply(
            "Вы начали новую операцию без завершения предыдущей. Ваш предыдущий процесс был сброшен."
        )
        await state.finish()


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
    dp.register_callback_query_handler(
        cancel_handler, lambda c: c.data.startswith("cancel"), state="*"
    )
    dp.register_callback_query_handler(
        handle_manage_menu, lambda c: c.data.startswith("manager")
    )
    dp.register_callback_query_handler(
        send_user_request_to_manager, lambda c: c.data.startswith("call_support")
    )