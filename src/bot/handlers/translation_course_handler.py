import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from decouple import config
from api.translation_course_api import get_before_course, get_after_course
from config import bot
from datetime import datetime
from keyboards.base_kb import after_translation_course, cancel_keyboard


BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

course_cb = CallbackData("course", "type")

file_paths = {}


async def list_courses(callback_query: types.CallbackQuery, callback_data: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("До 100’000 юаней", callback_data=course_cb.new(type="before"))
    )
    keyboard.add(
        InlineKeyboardButton("Свыше 100’000 юаней", callback_data=course_cb.new(type="after"))
    ),


    await bot.edit_message_text(
        "Выберите категорию курса:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard,
    )

def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        return "N/A"

async def send_course(callback_query: types.CallbackQuery, callback_data: dict):
    course_type = callback_data["type"]

    if course_type == "before":
        course = await get_before_course()
    else:
        course = await get_after_course()

    if not course:
        await bot.send_message(callback_query.from_user.id, "Курс не найден.")
        return

    rub_yuan = course.get("rub_yuan", "N/A")
    som_yuan = course.get("som_yuan", "N/A")
    updated_at = format_date(course.get("updated_at", "N/A"))

    response_message = (
        f"*Курс {course_type == 'before' and 'до 100’000 юаней' or 'свыше 100’000 юаней'}*\n\n"
        f"**Рубль - Юань:** `{rub_yuan}`\n"
        f"**Сом - Юань:** `{som_yuan}`\n"
        f"**Дата обновления курса:** `{updated_at}`"
    )

    await callback_query.message.edit_text(
        response_message,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=after_translation_course()  # предполагая, что это возвращает InlineKeyboardMarkup
    )

def register_course_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        lambda c: list_courses(c, callback_data={}), Text(equals="list_courses")
    )
    dp.register_callback_query_handler(send_course, course_cb.filter())
