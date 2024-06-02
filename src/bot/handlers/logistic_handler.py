from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api.logistic_api import *
from keyboards.logistic_kb import *
from keyboards.base_kb import after_logistic_request_menu
from utils import format_logistic_request

from config import bot


class LogisticsForm(StatesGroup):
    cargo_type = State()
    weight = State()
    volume = State()
    packaging_type = State()
    insurance_cost = State()


async def calculate_logistics_start(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    cargo_types = await fetch_cargo_types()
    keyboard = select_type(cargo_types)
    message = await bot.send_message(
        callback_query.from_user.id, "Выберите тип груза:", reply_markup=keyboard
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
        callback_query.from_user.id, "Введите вес груза в кг:"
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.weight.set()


async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    user_data = await state.get_data()
    await bot.delete_message(message.chat.id, user_data["last_message_id"])
    new_message = await message.answer("Введите объем груза в кубических метрах:")
    await state.update_data(last_message_id=new_message.message_id)
    await LogisticsForm.volume.set()


async def set_volume(message: types.Message, state: FSMContext):
    await state.update_data(volume=message.text)
    user_data = await state.get_data()
    await bot.delete_message(message.chat.id, user_data["last_message_id"])
    packaging_types = await fetch_packaging_types()
    keyboard = select_packaging(packaging_types)
    new_message = await message.answer("Выберите вид упаковки:", reply_markup=keyboard)
    await state.update_data(last_message_id=new_message.message_id)
    await LogisticsForm.packaging_type.set()


async def set_packaging_type(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    await state.update_data(packaging_type_id=packaging_id)
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.delete_message(callback_query.from_user.id, user_data["last_message_id"])
    message = await bot.send_message(
        callback_query.from_user.id, "Введите стоимость товара для расчета страховки:"
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.insurance_cost.set()


async def set_insurance_cost(message: types.Message, state: FSMContext):
    await state.update_data(price_before_insurance=message.text)
    user_data = await state.get_data()
    await bot.delete_message(message.chat.id, user_data["last_message_id"])
    api_data = {
        "tg_client_id": message.from_user.id,  # Telegram user ID
        "cargo_type_id": user_data["cargo_type_id"],
        "cargo_package_type_id": user_data["packaging_type_id"],
        "weight": float(user_data["weight"]),
        "volume": float(user_data["volume"]),
        "price_before_insurance": float(user_data["price_before_insurance"]),
    }
    api_response = await create_logistic_request(api_data)
    response_data = format_logistic_request(api_response)
    keyboard = after_logistic_request_menu()
    await message.reply(response_data)
    await state.finish()
    await bot.send_message(
        message.chat.id, text="Выберите действие", reply_markup=keyboard
    )


def register_logistics_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        calculate_logistics_start, lambda c: c.data == "calculate_logistics"
    )
    dp.register_callback_query_handler(
        set_cargo_type,
        lambda c: c.data.startswith("cargo_"),
        state=LogisticsForm.cargo_type,
    )
    dp.register_message_handler(set_weight, state=LogisticsForm.weight)
    dp.register_message_handler(set_volume, state=LogisticsForm.volume)
    dp.register_callback_query_handler(
        set_packaging_type,
        lambda c: c.data.startswith("packaging_"),
        state=LogisticsForm.packaging_type,
    )
    dp.register_message_handler(set_insurance_cost, state=LogisticsForm.insurance_cost)
