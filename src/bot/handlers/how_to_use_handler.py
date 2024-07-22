import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.how_to_use_api import get_how_to_useinfo
from config import bot
from keyboards.base_kb import main_menu_keyboard, single_menu_button
from aiogram.utils.markdown import text, bold

async def get_how_to_use_info_handler(callback_query: types.CallbackQuery):
    how_to_use = await get_how_to_useinfo()
    
    if not how_to_use:
        await callback_query.message.edit_text(
            text="/help тебе поможет",
            reply_markup=main_menu_keyboard()
        )
        return

    text_message = how_to_use.get("text")
    await callback_query.message.edit_text(
        text=text_message,
        reply_markup=single_menu_button(),
    )

def register_how_to_use_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_how_to_use_info_handler, Text(equals="how_to_use"))
