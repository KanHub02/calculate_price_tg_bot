from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def yes_no_keyboard():
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text="Да ✅", callback_data="yes")
    no_button = InlineKeyboardButton(text="Нет ❌", callback_data="no")
    keyboard.add(yes_button, no_button)
    return keyboard


def answerkb():
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text="Да ✅", callback_data="Да")
    no_button = InlineKeyboardButton(text="Нет ❌", callback_data="Нет")
    keyboard.add(yes_button, no_button)
    return keyboard


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            text="Рассчитать Логистику 🚚", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(
            text="Рассчитать Фулфилмент 📦", callback_data="calculate_fulfillment"
        ),
        InlineKeyboardButton(text="Курс перевода 💱", callback_data="exchange_rate"),
        InlineKeyboardButton(text="Полезности 💡", callback_data="utilities"),
        InlineKeyboardButton(text="Менеджер 👨‍💼", callback_data="manager"),
        InlineKeyboardButton(text="Условия работы 📋", callback_data="work_conditions"),
        InlineKeyboardButton(text="Стать Партнером 🤝", callback_data="become_partner"),
        InlineKeyboardButton(
            text="Как пользоваться ботом? 🤔", callback_data="how_to_use"
        ),
    ]
    # Все кнопки будут располагаться в одной колонке
    for button in buttons:
        keyboard.add(button)
    return keyboard


def utilities_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Каталоги 📚", callback_data="catalog"),
        InlineKeyboardButton(
            text="Полезные статьи 📝", callback_data="useful_articles"
        ),
        InlineKeyboardButton(text="Остальное 🧩", callback_data="list_others"),
        InlineKeyboardButton(
            text="Оставить обратную связь 💬", callback_data="usefull_feedback"
        ),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2], buttons[3])
    keyboard.add(buttons[4])
    return keyboard


def manager_menu_keyboards():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            text="Связаться с менеджером 📞", callback_data="call_support"
        ),
        InlineKeyboardButton(text="Мошенники? 🚨", callback_data="scammers"),
        InlineKeyboardButton(text="Оставить отзыв ✍️", callback_data="set_review"),
    ]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2])
    return keyboard


def after_translation_course():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            text="Курс перевода 💵", callback_data="list_courses"
        ),
        InlineKeyboardButton(
            text="Оплата в $ и Криптовалюте 💵", callback_data="crypto_translate"
        ),
        InlineKeyboardButton(
            text="Переводы между РФ-КР 🇷🇺🇰🇬", callback_data="rf_kg_translate"
        ),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    keyboard.add(buttons[0], buttons[1], buttons[2])
    keyboard.add(buttons[3])
    return keyboard


def after_logistic_request_menu():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            text="Просчитать другой товар 📊", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(text="Вызвать менеджера 👨‍💼", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2])
    return keyboard


def after_working_conditions():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Менеджер 👨‍💼", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    keyboard.add(buttons[0], buttons[1])
    return keyboard


def after_ff_request_menu():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            text="Просчитать другой товар 📊", callback_data="calculate_fulfillment"
        ),
        InlineKeyboardButton(text="Вызвать менеджера 👨‍💼", callback_data="manager"),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    keyboard.add(buttons[0], buttons[1])
    keyboard.add(buttons[2])
    return keyboard


def cancel_keyboard():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Отменить ❌", callback_data="cancel"),
    ]
    keyboard.add(*buttons)
    return keyboard
