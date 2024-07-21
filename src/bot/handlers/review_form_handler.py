import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.review_form_api import get_review_form
from api.base import get_manager_card_list
from config import bot
from keyboards.base_kb import main_menu_keyboard
from aiogram.utils.markdown import text, bold, escape_md

async def review_form(callback_query: types.CallbackQuery):
    manager_card = await get_manager_card_list()
    if len(manager_card) <= 0:
        manager_card = None
    else:
        manager_card = manager_card[0]

    manager_card_text = text(
        bold("Username:"), escape_md(manager_card.get('tg_username')),
        bold("\nID:"), escape_md(manager_card.get('tg_id'))
    )
    link_to_form = await get_review_form()
    link_to_form = link_to_form[0].get("link")
    message = text(
        f"📌 Если у вас появилась спорная ситуация, вы можете обратиться к менеджеру:\n",
    manager_card_text,
        f"\n\n📝 Или заполнить форму по ссылке: {link_to_form}"
    )
    await callback_query.message.edit_text(
        text=message,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
    
def register_review_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(review_form, Text(equals="set_review"))
