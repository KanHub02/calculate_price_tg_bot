from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_catalog_category(catalog_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=category["title"], callback_data=f"calalog_category_{category['id']}"
        )
        for category in catalog_categories
    ]
    keyboard.add(*buttons)
    return keyboard
