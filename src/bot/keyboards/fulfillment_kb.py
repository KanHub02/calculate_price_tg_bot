from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_marking_type(marking_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=marking["title"], callback_data=f"marking_{marking['id']}"
        )
        for marking in marking_types
    ]
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
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
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
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
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
    keyboard.add(*buttons)
    return keyboard


def select_packaging_sizes(sizes):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=size["size"], callback_data=f"size_{size['size']}")
        for size in sizes
    ]
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    buttons.append(cancel_button)
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
    cancel_button = InlineKeyboardButton(
        text="Отменить ❌", callback_data="cancel"
    )
    keyboard.add(other_button)
    keyboard.add(cancel_button)
    return keyboard


def after_ff_state_keyboard():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Вызвать венеджера 👨‍💼", callback_data="manager"),
        InlineKeyboardButton(text="Просчитать другой товар 📦", callback_data="main_menu"),
        InlineKeyboardButton(text="Главное меню 🏠", callback_data="main_menu"),
    ]
    for button in buttons:
        keyboard.add(button)
    return keyboard