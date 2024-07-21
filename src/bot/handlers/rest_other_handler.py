import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from decouple import config
from api.article_api import get_rest_other_list
from config import bot

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

other_cb = CallbackData("other", "id", "page")
rest_other_pagination_cb = CallbackData("rest_other_pagination", "page")
menu_cb = CallbackData("menu", "action")

OTHERS_PER_PAGE = 5

file_paths = {}


async def list_others(callback_query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page", 1))
    others = await get_rest_other_list()

    total_others = len(others)
    total_pages = (total_others + OTHERS_PER_PAGE - 1) // OTHERS_PER_PAGE

    start_idx = (page - 1) * OTHERS_PER_PAGE
    end_idx = start_idx + OTHERS_PER_PAGE
    page_others = others[start_idx:end_idx]

    keyboard = InlineKeyboardMarkup(row_width=1)
    for other in page_others:
        file_id = str(other["id"])
        file_paths[file_id] = other["file"]
        keyboard.add(
            InlineKeyboardButton(
                other["title"], callback_data=other_cb.new(id=file_id, page=page)
            )
        )

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Назад", callback_data=rest_other_pagination_cb.new(page=page - 1)
            )
        )
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Вперед", callback_data=rest_other_pagination_cb.new(page=page + 1)
            )
        )

    keyboard.add(*pagination_buttons)
    keyboard.add(
        InlineKeyboardButton(
            "Вернуться в меню", callback_data=menu_cb.new(action="main_menu")
        )
    )
    await bot.edit_message_text(
        f"Страница {page} из {total_pages}. Выберите файл:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard,
    )


async def send_file(callback_query: types.CallbackQuery, callback_data: dict):
    logging.info(f"send_file called with callback_data: {callback_data}")
    file_id = callback_data["id"]
    file_path = file_paths.get(file_id)

    if not file_path:
        await bot.send_message(callback_query.from_user.id, "Файл не найден.")
        return

    logging.info(f"Original file_path: {file_path}")

    if file_path.startswith("http"):
        file_url = file_path
    else:
        file_url = f"{BACKEND_ADDRESS}/media/{file_path.lstrip('/media/')}"

    logging.info(f"Formatted file_url: {file_url}")

    local_file_path = f"temp_{os.path.basename(file_path)}"

    try:
        await bot.send_message(
            callback_query.from_user.id, "⏳ Пожалуйста, подождите..."
        )

        await download_file(file_url, local_file_path)

        await bot.send_document(
            callback_query.from_user.id, types.InputFile(local_file_path)
        )

        if os.path.exists(local_file_path):
            os.remove(local_file_path)

    except Exception as e:
        logging.error(f"Error downloading or sending file: {e}")
        await bot.send_message(
            callback_query.from_user.id, "Ошибка при обработке файла."
        )

        if os.path.exists(local_file_path):
            os.remove(local_file_path)


async def download_file(url, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(destination, "wb") as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                return destination
            else:
                raise Exception(
                    f"Failed to download file with status {response.status}"
                )


def register_rest_other_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        lambda c: list_others(c, callback_data={"page": 1}), Text(equals="list_others")
    )
    dp.register_callback_query_handler(list_others, rest_other_pagination_cb.filter())
    dp.register_callback_query_handler(send_file, other_cb.filter())
