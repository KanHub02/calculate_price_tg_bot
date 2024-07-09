from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from decouple import config


def select_marking_type(marking_types):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    buttons = [
        InlineKeyboardButton(
            text=marking["title"]
        )
        for marking in marking_types
    ]
    keyboard.add(*buttons)
    return keyboard


def select_checkdefect_type(check_defect_types):
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
    buttons = [
        InlineKeyboardButton(
            text=defect_type["title"]
        )
        for defect_type in check_defect_types
    ]
    keyboard.add(*buttons)
    return keyboard


def select_packaging_option(packaging_options):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=packaging["title"], callback_data=f"packaging_{packaging['id']}"
        )
        for packaging in packaging_options
    ]
    keyboard.add(*buttons)
    return keyboard


def select_packaging_sizes(sizes):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=size["size"], callback_data=f"size_{size['size']}")
        for size in sizes
    ]
    keyboard.add(*buttons)
    return keyboard


def select_warehouse_keyboard(warehouses):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for warehouse in warehouses:
        button = InlineKeyboardButton(
            text=warehouse["title"], callback_data=f"warehouse_{warehouse['id']}"
        )
        keyboard.add(button)
    return keyboard
