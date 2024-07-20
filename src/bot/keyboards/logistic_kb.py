from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_type(cargo_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=cargo_type["title"], callback_data=f"cargo_{cargo_type['id']}"
        )
        for cargo_type in cargo_types
    ]
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
    keyboard.add(*buttons)
    return keyboard

def select_packaging(packaging_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=packaging["title"], callback_data=f"packaging_{packaging['id']}"
        )
        for packaging in packaging_types
    ]
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
    keyboard.add(*buttons)
    return keyboard
