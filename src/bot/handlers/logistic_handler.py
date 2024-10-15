import logging

from aiogram import types, Dispatcher
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.base_kb import (
    after_logistic_request_menu,
    main_menu_keyboard,
    cancel_keyboard,
)
from keyboards.logistic_kb import select_packaging, select_type
from api.logistic_api import (
    fetch_cargo_types,
    create_logistic_request,
    fetch_packaging_types,
)
from utils import format_logistic_request
from config import bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LOGISTIC_SERVICE")


class LogisticsForm(StatesGroup):
    cargo_type = State()
    weight = State()
    volume = State()
    packaging_type = State()
    insurance_cost = State()


async def fetch_and_check(api_call, error_message):
    result = await api_call()
    if len(result) <= 0:
        return None, error_message
    return result, ""


async def calculate_logistics_start(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    cargo_types, error = await fetch_and_check(
        fetch_cargo_types, "Типы грузы не найдены, пожалуйста, попробуйте позже."
    )
    if error:
        await bot.send_message(callback_query.from_user.id, error)
        await state.finish()
        return
    keyboard = select_type(cargo_types)
    message = await callback_query.message.edit_text(
        "Выберите тип груза:", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.cargo_type.set()


async def set_cargo_type(callback_query: types.CallbackQuery, state: FSMContext):
    cargo_id = callback_query.data.split("_")[1]
    await state.update_data(cargo_type_id=cargo_id)
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.delete_message(callback_query.from_user.id, user_data["last_message_id"])
    message = await bot.send_message(
        callback_query.from_user.id,
        "Введите вес груза в кг:",
        reply_markup=cancel_keyboard(),
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.weight.set()


async def set_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight=weight)
    except ValueError:
        await message.reply(
            "Пожалуйста, введите правильное значение веса. К примеру 1.1"
        )
        return

    user_data = await state.get_data()
    await bot.delete_message(message.chat.id, user_data["last_message_id"])
    new_message = await message.answer(
        "Введите объем груза в кубических метрах:", reply_markup=cancel_keyboard()
    )
    await state.update_data(last_message_id=new_message.message_id)
    await LogisticsForm.volume.set()


async def set_volume(message: types.Message, state: FSMContext):
    try:
        volume = float(message.text)
        await state.update_data(volume=volume)
        user_data = await state.get_data()
        await bot.delete_message(message.chat.id, user_data["last_message_id"])
    except ValueError:
        await message.reply("Пожалуйста, введите правильное значение объема.")
        return

    package_types = await fetch_packaging_types()
    keyboard = select_packaging(package_types)
    new_message = await message.answer("Выберите вид упаковки:", reply_markup=keyboard)
    await state.update_data(last_message_id=new_message.message_id)
    await LogisticsForm.packaging_type.set()


async def set_packaging_type(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_type = callback_query.data.split("_")[1]
    await state.update_data(packaging_type=packaging_type)
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.delete_message(callback_query.from_user.id, user_data["last_message_id"])
    message = await bot.send_message(
        callback_query.from_user.id,
        "Введите стоимость товара для расчета страховки:",
        reply_markup=cancel_keyboard(),
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.insurance_cost.set()


async def set_insurance_cost(message: types.Message, state: FSMContext):
    try:
        insurance_cost = float(message.text)
        await state.update_data(price_before_insurance=insurance_cost)
    except ValueError:
        await message.reply("Пожалуйста, введите правильное значение стоимости.")
        return

    user_data = await state.get_data()
    await bot.delete_message(message.chat.id, user_data["last_message_id"])
    api_data = {
        "tg_client_id": message.from_user.id,
        "cargo_type_id": user_data["cargo_type_id"],
        "cargo_package_type_id": user_data["packaging_type"],
        "weight": user_data["weight"],
        "volume": user_data["volume"],
        "price_before_insurance": user_data["price_before_insurance"],
    }
    logger.info(str(api_data))
    api_response = await create_logistic_request(api_data)
    response_data = format_logistic_request(api_response)
    keyboard = after_logistic_request_menu()
    await message.reply(response_data, parse_mode=ParseMode.MARKDOWN_V2)
    await state.finish()
    await bot.send_message(
        message.chat.id, text="Что дальше? 🤔", reply_markup=keyboard
    )


async def handle_any_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == LogisticsForm.weight.state:
        await set_weight(message, state)
    elif current_state == LogisticsForm.volume.state:
        await set_volume(message, state)
    elif current_state == LogisticsForm.insurance_cost.state:
        await set_insurance_cost(message, state)


def register_logistics_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        calculate_logistics_start, lambda c: c.data == "calculate_logistics"
    )
    dp.register_callback_query_handler(
        set_cargo_type,
        lambda c: c.data.startswith("cargo_"),
        state=LogisticsForm.cargo_type,
    )
    dp.register_callback_query_handler(
        set_packaging_type,
        lambda c: c.data.startswith("packaging_"),
        state=LogisticsForm.packaging_type,
    )
    dp.register_message_handler(set_weight, state=LogisticsForm.weight)
    dp.register_message_handler(set_volume, state=LogisticsForm.volume)
    dp.register_message_handler(set_insurance_cost, state=LogisticsForm.insurance_cost)
