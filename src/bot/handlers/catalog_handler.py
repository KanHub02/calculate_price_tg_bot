from aiogram import types, Dispatcher

from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from decouple import config

from config import bot, dp
from api.catalog_api import get_catalog_list, get_catalog_products
from keyboards.catalog_kb import select_catalog_category
import aiohttp
import os

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


category_cb = CallbackData("category", "id")
product_cb = CallbackData("product", "id")


async def choose_category(callback_query: types.CallbackQuery):
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
            raise Exception(f"Failed to download file with status {response.status}")


# Send products to the user after a category is chosen
async def list_products(callback_query: types.CallbackQuery, callback_data: dict):
    category_id = callback_data["id"]
    products = await get_catalog_products(category_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=product["title"], callback_data=product_cb.new(id=product["file"])
        )
        for product in products["products"]
    ]
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id, "Выберите продукт:", reply_markup=keyboard
    )


# Send the PDF file of the selected product
async def send_pdf(callback_query: types.CallbackQuery, callback_data: dict):
    file_path = callback_data["id"]
    pdf_url = f"{BACKEND_ADDRESS}/media/{file_path}"
    local_file_path = f"temp_{file_path}"

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
        await bot.send_message(
            callback_query.from_user.id, "Ошибка при обработке файла."
        )

        if os.path.exists(local_file_path):
            os.remove(local_file_path)


def register_catalof_handler(dp: Dispatcher):
    dp.register_callback_query_handler(choose_category, Text(startswith="catalog"))
    dp.register_callback_query_handler(list_products, category_cb.filter())
    dp.register_callback_query_handler(send_pdf, product_cb.filter())
