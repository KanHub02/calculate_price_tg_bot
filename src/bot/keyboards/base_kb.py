from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from decouple import config


def yes_no_keyboard():
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text="Да")
    no_button = InlineKeyboardButton(text="Нет")
    keyboard.add(yes_button, no_button)
    return keyboard


def answerkb():
    answerkb = ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=False
    )
    answeryes = KeyboardButton(text="Да")
    answerno = KeyboardButton(text="Нет")
    answerkb.add(answerno, answeryes)
    return answerkb


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Рассчитать Логистику", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(
            text="Рассчитать Фулфилмент", callback_data="calculate_fulfillment"
        ),
        InlineKeyboardButton(text="Курс перевода", callback_data="exchange_rate"),
        InlineKeyboardButton(text="Полезности", callback_data="utilities"),
        InlineKeyboardButton(text="Менеджер", callback_data="manager"),
        InlineKeyboardButton(text="Условия работы", callback_data="work_conditions"),
        InlineKeyboardButton(text="Стать Партнером", callback_data="become_partner"),
        InlineKeyboardButton(
            text="Как пользоваться ботом?", callback_data="how_to_use"
        ),
    ]
    keyboard.add(*buttons)
    return keyboard


def utilities_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Каталоги", callback_data="catalog"),
        InlineKeyboardButton(text="Полезные статьи", callback_data="useful_articles"),
        InlineKeyboardButton(text="Остальное", callback_data="other"),
        InlineKeyboardButton(
            text="Оставить обратную связь", callback_data="usefull_feedback"
        ),
    ]
    keyboard.add(*buttons)
    return keyboard


def manager_menu_keyboards():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Связаться с менеджером", callback_data="call_support"
        ),
        InlineKeyboardButton(text="Мошенники ?", callback_data="scammers"),
        InlineKeyboardButton(text="Оставить отзыв", callback_data="set_review"),
    ]

    keyboard.add(*buttons)
    return keyboard


def after_translation_course():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Оплата в $ и Криптовалюте", callback_data="crypto_translate"
        ),
        InlineKeyboardButton(
            text="Переводы между РФ-КР", callback_data="rf_kg_translate"
        ),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ]

    keyboard.add(*buttons)
    return keyboard


def after_logistic_request_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Просчитать другой товар", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(text="Вызвать менеджера", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ]
    keyboard.add(*buttons)
    return keyboard


def after_working_conditions():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Менеджер", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ]
    keyboard.add(*buttons)
    return keyboard


def after_ff_request_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Просчитать другой товар", callback_data="calculate_fulfillment"
        ),
        InlineKeyboardButton(text="Вызвать менеджера", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ]
    keyboard.add(*buttons)
    return keyboard
