import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.working_condition_api import get_working_condition_info
from config import bot
from keyboards.base_kb import main_menu_keyboard, single_menu_button
from aiogram.utils.markdown import bold, text as md_text


async def get_working_condition_handler(callback_query: types.CallbackQuery):
    working_condition_article = await get_working_condition_info()
    
    if not working_condition_article:
        await callback_query.message.edit_text(
            text="В скором времени мы подготовим статью об этом!",
            reply_markup=main_menu_keyboard()
        )
    
    link_message = working_condition_article.get("text")
    await callback_query.message.edit_text(
            text=link_message,
            reply_markup=single_menu_button()
        )

def register_working_condition_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_working_condition_handler, Text(equals="work_conditions"))
