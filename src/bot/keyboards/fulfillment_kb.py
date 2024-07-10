from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_marking_type(marking_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=marking["title"], callback_data=f"marking_{marking['id']}"
        )
        for marking in marking_types
    ]
    keyboard.add(*buttons)
    return keyboard


def select_checkdefect_type(check_defect_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=defect_type["title"], callback_data=f"defect_{defect_type['id']}"
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
    keyboard = InlineKeyboardMarkup(row_width=1)
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
    other_button = InlineKeyboardButton(text="Другое", callback_data="warehouse_other")
    keyboard.add(other_button)
    return keyboard
