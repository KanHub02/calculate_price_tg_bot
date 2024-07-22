import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.partner_lead_api import get_partner_lead_info as get_partner_lead_api
from config import bot
from keyboards.base_kb import main_menu_keyboard, single_menu_button
from aiogram.utils.markdown import bold, text as md_text


async def get_partner_lead_info(callback_query: types.CallbackQuery):
    partner_lead_article = await get_partner_lead_api()
    
    if not partner_lead_article:
        await callback_query.message.edit_text(
            text="Ожидайте! В скором времени мы подготовим статью об этом!",
            reply_markup=main_menu_keyboard()
        )
    
    link_message = partner_lead_article.get("link")
    await callback_query.message.edit_text(
            text=link_message,
            reply_markup=single_menu_button()
        )

def register_partner_lead_info_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_partner_lead_info, Text(equals="become_partner"))
