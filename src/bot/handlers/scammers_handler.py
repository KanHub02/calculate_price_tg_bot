import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.scammers_api import get_about_scammers_info
from config import bot
from keyboards.base_kb import main_menu_keyboard
from aiogram.utils.markdown import bold, text as md_text


async def get_scammers_info(callback_query: types.CallbackQuery):
    scammers_article = await get_about_scammers_info()
    
    if not scammers_article:
        await callback_query.message.edit_text(
            text="Будьте осторожней! В скором времени мы подготовим статью об этом!",
            reply_markup=main_menu_keyboard()
        )
    
    link_message = scammers_article.get("link")
    await callback_query.message.edit_text(
            text=link_message,
            reply_markup=main_menu_keyboard()
        )

def register_scammers_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_scammers_info, Text(equals="scammers"))
