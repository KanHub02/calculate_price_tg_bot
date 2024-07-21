import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.translation_info_api import get_crypto_info, get_rf_info
from config import bot
from keyboards.base_kb import after_translation_course
from aiogram.utils.markdown import bold, text as md_text

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

translate_cb = CallbackData("translate", "type")

async def list_rf_translation(callback_query: types.CallbackQuery):
    translation = await get_rf_info()

    if not translation:
        await bot.send_message(callback_query.from_user.id, "Информация не найдена.")
        return

    text = translation.get("text", "N/A")

    # Форматируем текст с помощью Markdown
    formatted_text = md_text(bold("Информация по переводам между РФ-КР"), "\n\n", text)

    await callback_query.message.edit_text(
        formatted_text,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=after_translation_course()
    )

async def list_crypto_translation(callback_query: types.CallbackQuery):
    translation = await get_crypto_info()

    if not translation:
        await bot.send_message(callback_query.from_user.id, "Информация не найдена.")
        return

    text = translation.get("text", "N/A")

    # Форматируем текст с помощью Markdown
    formatted_text = md_text(bold("Информация по оплате в $ и Криптовалюте"), "\n\n", text)

    await callback_query.message.edit_text(
        formatted_text,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=after_translation_course()
    )


def register_translation_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        list_rf_translation, Text(equals="rf_kg_translate")
    )
    dp.register_callback_query_handler(
        list_crypto_translation, Text(equals="crypto_translate")
    )
