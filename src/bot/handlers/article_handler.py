import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from decouple import config
from api.article_api import get_article_list, get_article_detail, get_rest_other_list
from handlers.base import handle_main_menu
from config import bot


article_cb = CallbackData("article", "id", "page")
pagination_cb = CallbackData("pagination", "page")
menu_cb = CallbackData("menu", "action")

ARTICLES_PER_PAGE = 5


async def list_articles(callback_query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page", 1))
    articles = await get_article_list()

    total_articles = len(articles)
    total_pages = (total_articles + ARTICLES_PER_PAGE - 1) // ARTICLES_PER_PAGE

    start_idx = (page - 1) * ARTICLES_PER_PAGE
    end_idx = start_idx + ARTICLES_PER_PAGE
    page_articles = articles[start_idx:end_idx]

    keyboard = InlineKeyboardMarkup(row_width=1)
    for article in page_articles:
        keyboard.add(
            InlineKeyboardButton(
                article["title"],
                callback_data=article_cb.new(id=article["id"], page=page),
            )
        )

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Назад", callback_data=pagination_cb.new(page=page - 1)
            )
        )
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(
                "Вперед", callback_data=pagination_cb.new(page=page + 1)
            )
        )

    keyboard.add(*pagination_buttons)
    keyboard.add(
        InlineKeyboardButton(
            "Вернуться в меню", callback_data=menu_cb.new(action="main_menu")
        )
    )

    await bot.edit_message_text(
        f"Страница {page} из {total_pages}. Выберите статью:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard,
    )


async def show_article(callback_query: types.CallbackQuery, callback_data: dict):
    article_id = callback_data["id"]
    article = await get_article_detail(article_id)

    if article:
        await bot.send_message(
            callback_query.from_user.id,
            f"Описание: {article['description']}\n{article['link']}",
        )
    else:
        await bot.send_message(callback_query.from_user.id, "Статья не найдена.")


def register_articles_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(list_articles, pagination_cb.filter())
    dp.register_callback_query_handler(show_article, article_cb.filter())
    dp.register_callback_query_handler(
        lambda c: list_articles(c, callback_data={"page": 1}),
        Text(equals="useful_articles"),
    )
    dp.register_callback_query_handler(
        handle_main_menu, menu_cb.filter(action="main_menu")
    )
