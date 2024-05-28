from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api.logistic_api import *
from keyboards.logistic_kb import *
from keyboards.base_kb import main_menu_keyboard
from utils import format_logistic_request

from config import bot

class LogisticsForm(StatesGroup):
    phone_number = State()
    cargo_type = State()
    packaging_type = State()
    title = State()
    weight = State()
    volume = State()
    quantity = State()
    insurance_cost = State()

async def calculate_logistics_start(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    cargo_types = await fetch_cargo_types()
    keyboard = select_type(cargo_types)
    message = await bot.send_message(
        callback_query.from_user.id, "Выберите тип груза:", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.cargo_type.set()

async def set_cargo_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    cargo_id = callback_query.data.split("_")[1]
    cargo_types = await fetch_cargo_types()
    cargo_type = next((ct for ct in cargo_types if ct["id"] == cargo_id), None)
    if cargo_type:
        await state.update_data(cargo_type_id=cargo_id, cargo_type=cargo_type["title"])

    packaging_types = await fetch_packaging_types()
    keyboard = select_packaging(packaging_types)
    message = await bot.send_message(
        callback_query.from_user.id, "Выберите вид упаковки:", reply_markup=keyboard
    )
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.packaging_type.set()
    await bot.answer_callback_query(callback_query.id)

async def set_packaging_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    packaging_id = callback_query.data.split("_")[1]
    packaging_types = await fetch_packaging_types()
    packaging_type = next(
        (pt for pt in packaging_types if pt["id"] == packaging_id), None
    )
    if packaging_type:
        await state.update_data(
            packaging_type_id=packaging_id, packaging_type=packaging_type["title"]
        )
    message = await bot.send_message(callback_query.from_user.id, "Введите номер телефона.")
    await state.update_data(last_message_id=message.message_id)
    await LogisticsForm.phone_number.set()
    await bot.answer_callback_query(callback_query.id)

async def set_phone_number(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    await state.update_data(phone_number=message.text)
    new_message = await message.answer("Введите название товара.")
    await state.update_data(last_message_id=new_message.message_id)
    await LogisticsForm.title.set()

async def set_title(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Введите вес груза в кг.")
    await state.update_data(title=message.text, last_message_id=new_message.message_id)
    await LogisticsForm.weight.set()

async def set_weight(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Введите объем груза в кубических метрах.")
    await state.update_data(weight=message.text, last_message_id=new_message.message_id)
    await LogisticsForm.volume.set()

async def set_volume(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Введите количество товара.")
    await state.update_data(volume=message.text, last_message_id=new_message.message_id)
    await LogisticsForm.quantity.set()

async def set_quantity(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Введите стоимость товара для расчета страховки.")
    await state.update_data(quantity=message.text, last_message_id=new_message.message_id)
    await LogisticsForm.insurance_cost.set()

async def set_insurance_cost(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    await state.update_data(insurance_cost=message.text)
    api_data = {
        "tg_client_id": message.from_user.id,
        "cargo_type_id": user_data["cargo_type_id"],
        "cargo_package_type_id": user_data["packaging_type_id"],
        "weight": user_data["weight"],
        "quantity": user_data["quantity"],
        "volume": user_data["volume"],
        "insurance_cost": user_data["insurance_cost"],
    }
    api_response = await create_logistic_request(api_data)
    response_data = format_logistic_request(api_response)
    await message.reply(f"{response_data}")
    keyboard = main_menu_keyboard()
    await message.reply("Выберите действие:", reply_markup=keyboard)
    await state.finish()

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
    dp.register_message_handler(set_phone_number, state=LogisticsForm.phone_number)
    dp.register_message_handler(set_title, state=LogisticsForm.title)
    dp.register_message_handler(set_weight, state=LogisticsForm.weight)
    dp.register_message_handler(set_volume, state=LogisticsForm.volume)
    dp.register_message_handler(set_quantity, state=LogisticsForm.quantity)
    dp.register_message_handler(set_insurance_cost, state=LogisticsForm.insurance_cost)
