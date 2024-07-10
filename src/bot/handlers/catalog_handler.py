from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from decouple import config
from config import bot, dp
from api.catalog_api import get_catalog_list, get_catalog_products, get_subcategory_list
from handlers.base import handle_main_menu
import aiohttp
import os
import uuid
import logging
import math

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

category_cb = CallbackData("category", "id")
subcategory_cb = CallbackData("subcategory", "id")
product_cb = CallbackData("product", "id", "page")
pagination_cb = CallbackData("pagination", "id", "page")

file_paths = {}

logging.basicConfig(level=logging.INFO)


async def choose_category(callback_query: types.CallbackQuery):
    logging.info("choose_category called")
    catalog = await get_catalog_list()
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=category["title"], callback_data=category_cb.new(id=category["id"])
        )
        for category in catalog
    ]
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id, "Выберите категорию:", reply_markup=keyboard
    )


async def choose_subcategory(callback_query: types.CallbackQuery, callback_data: dict):
    logging.info(f"choose_subcategory called with callback_data: {callback_data}")
    category_id = callback_data["id"]
    subcategories = await get_subcategory_list(category_id)
    logging.info(f"Subcategories: {subcategories}")
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=subcategory["title"],
            callback_data=subcategory_cb.new(id=subcategory["id"]),
        )
        for subcategory in subcategories
    ]
    keyboard.add(*buttons)
    await bot.edit_message_text(
        "Выберите подкатегорию:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard,
    )


PRODUCTS_PER_PAGE = 10


async def list_products(callback_query: types.CallbackQuery, callback_data: dict):
    logging.info(f"list_products called with callback_data: {callback_data}")
    subcategory_id = callback_data["id"]
    page = int(callback_data.get("page", 1))
    products = await get_catalog_products(subcategory_id)
    logging.info(f"Products: {products}")

    total_products = len(products)
    total_pages = math.ceil(total_products / PRODUCTS_PER_PAGE)

    start_idx = (page - 1) * PRODUCTS_PER_PAGE
    end_idx = start_idx + PRODUCTS_PER_PAGE
    page_products = products[start_idx:end_idx]
    logging.info(f"Page products: {page_products}")

    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for product in page_products:
        file_id = str(uuid.uuid4())
        file_paths[file_id] = product["file"]
        buttons.append(
            InlineKeyboardButton(
                text=product["title"],
                callback_data=product_cb.new(id=file_id, page=page),
            )
        )
    keyboard.add(*buttons)

    pagination_buttons = []
    if start_idx > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Назад",
                callback_data=pagination_cb.new(id=subcategory_id, page=page - 1),
            )
        )

    if end_idx < total_products:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Вперед",
                callback_data=pagination_cb.new(id=subcategory_id, page=page + 1),
            )
        )

    keyboard.add(*pagination_buttons)
    keyboard.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu"))

    page_info = f"Страница {page} из {total_pages}"

    try:
        await bot.edit_message_text(
            f"Выберите продукт:\n\n{page_info}",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard,
        )
    except Exception as e:
        logging.error(f"Error editing message: {e}")


async def send_pdf(callback_query: types.CallbackQuery, callback_data: dict):
    logging.info(f"send_pdf called with callback_data: {callback_data}")
    file_id = callback_data["id"]
    file_path = file_paths.get(file_id)

    if not file_path:
        await bot.send_message(callback_query.from_user.id, "Файл не найден.")
        return

    # Логирование для отладки
    logging.info(f"Original file_path: {file_path}")

    # Убедитесь, что file_path не содержит дублирования URL
    if file_path.startswith("http"):
        pdf_url = file_path
    else:
        pdf_url = f"{BACKEND_ADDRESS}/media/{file_path.lstrip('/media/')}"

    # Логирование для отладки
    logging.info(f"Formatted pdf_url: {pdf_url}")

    local_file_path = f"temp_{os.path.basename(file_path)}"

    try:
        await bot.send_message(
            callback_query.from_user.id, "⏳ Пожалуйста, подождите..."
        )

        await download_file(pdf_url, local_file_path)

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
    """Download a file from a URL and save it locally."""
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


async def return_to_menu(callback_query: types.CallbackQuery):
    await handle_main_menu(callback_query)


def register_catalog_handler(dp: Dispatcher):
    dp.register_callback_query_handler(choose_category, Text(startswith="catalog"))
    dp.register_callback_query_handler(choose_subcategory, category_cb.filter())
    dp.register_callback_query_handler(list_products, subcategory_cb.filter())
    dp.register_callback_query_handler(list_products, pagination_cb.filter())
    dp.register_callback_query_handler(send_pdf, product_cb.filter())
    dp.register_callback_query_handler(return_to_menu, Text(equals="menu"))
