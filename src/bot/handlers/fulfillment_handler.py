from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from api.fulfillment_api import *
from keyboards.fulfillment_kb import *
from keyboards.base_kb import yes_no_keyboard, main_menu_keyboard
from utils import format_ff_response, is_float, is_not_empty

from config import bot

class FulfillmentForm(StatesGroup):
    product_name = State()
    quantity = State()
    marking_type = State()
    honest_sign = State()
    packaging = State()
    packaging_size = State()
    tagging = State()
    inserts = State()
    box_quantity = State()
    warehouse = State()

async def calculate_fulfillment_start(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    message = await bot.send_message(callback_query.from_user.id, "Let's start setting up your fulfillment. First, enter the product name.")
    await state.update_data(last_message_id=message.message_id)
    await FulfillmentForm.product_name.set()

async def set_product_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Product name received. Now, please enter the quantity.")
    await state.update_data(product_name=message.text, last_message_id=new_message.message_id)
    await FulfillmentForm.quantity.set()

async def set_quantity(message: types.Message, state: FSMContext):
    if not is_float(message.text):
        await message.reply("Please enter a valid numeric quantity.")
        return
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Quantity set. Please select a marking type.")
    marking_types = await fetch_marking_types()
    if not marking_types:
        await message.answer("No marking types found, please try again later.")
        await state.finish()
        return
    keyboard = select_marking_type(marking_types)
    await new_message.reply("Choose a marking type:", reply_markup=keyboard)
    await state.update_data(quantity=float(message.text), last_message_id=new_message.message_id)
    await FulfillmentForm.marking_type.set()

async def set_marking_type(callback_query: types.CallbackQuery, state: FSMContext):
    marking_id = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer("Marking type selected. Do you need an 'honest sign'?")
    keyboard = yes_no_keyboard()
    await new_message.reply("Choose your option:", reply_markup=keyboard)
    await state.update_data(marking_type_id=marking_id, last_message_id=new_message.message_id)
    await FulfillmentForm.honest_sign.set()

async def set_honest_sign(callback_query: types.CallbackQuery, state: FSMContext):
    honest_sign = callback_query.data == "yes"
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer(f"Honest sign {'enabled' if honest_sign else 'disabled'}. Next, how many units fit in a 60x40x40 box?")
    await state.update_data(honest_sign=honest_sign, last_message_id=new_message.message_id)
    await FulfillmentForm.box_quantity.set()

async def set_box_quantity(message: types.Message, state: FSMContext):
    if not is_float(message.text):
        await message.reply("Please enter a valid box quantity in numeric format.")
        return
    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=user_data['last_message_id'])
    new_message = await message.answer("Box quantity noted. Please select packaging type.")
    packaging_options = await fetch_packaging_options()
    if not packaging_options:
        await message.reply("No packaging options found, please try again later.")
        await state.finish()
        return
    keyboard = select_packaging_option(packaging_options)
    await new_message.reply("Choose packaging type:", reply_markup=keyboard)
    await state.update_data(box_quantity=float(message.text), last_message_id=new_message.message_id)
    await FulfillmentForm.packaging.set()

async def set_packaging(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer("Packaging type selected. Now, select the size of the packaging.")
    sizes = await fetch_packaging_sizes(packaging_id)
    keyboard = select_packaging_sizes(sizes)
    await new_message.reply("Choose the size of the packaging:", reply_markup=keyboard)
    await state.update_data(packaging_id=packaging_id, last_message_id=new_message.message_id)
    await FulfillmentForm.packaging_size.set()

async def set_packaging_size(callback_query: types.CallbackQuery, state: FSMContext):
    size = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer("Packaging size selected. Do you need tagging?")
    keyboard = yes_no_keyboard()
    await new_message.reply("Please select:", reply_markup=keyboard)
    await state.update_data(packaging_size=size, last_message_id=new_message.message_id)
    await FulfillmentForm.tagging.set()

async def set_tagging(callback_query: types.CallbackQuery, state: FSMContext):
    tagging = callback_query.data == "yes"
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer("Tagging option noted. Do you need any inserts?")
    keyboard = yes_no_keyboard()
    await new_message.reply("Please select:", reply_markup=keyboard)
    await state.update_data(tagging=tagging, last_message_id=new_message.message_id)
    await FulfillmentForm.inserts.set()

async def set_inserts(callback_query: types.CallbackQuery, state: FSMContext):
    inserts = callback_query.data == "yes"
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    new_message = await callback_query.message.answer("Inserts option selected. Finally, select the warehouse for dispatch.")
    warehouses = await fetch_warehouses()
    keyboard = select_warehouse_keyboard(warehouses)
    await new_message.reply("Choose the warehouse:", reply_markup=keyboard)
    await state.update_data(inserts=inserts, last_message_id=new_message.message_id)
    await FulfillmentForm.warehouse.set()

async def set_warehouse(callback_query: types.CallbackQuery, state: FSMContext):
    warehouse_id = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=user_data['last_message_id'])
    ff_data = await format_ff_response({
        "warehouse_id": warehouse_id,
        "product_name": user_data["product_name"],
        "quantity": user_data["quantity"],
        "marking_type_id": user_data["marking_type_id"],
        "honest_sign": user_data["honest_sign"],
        "box_quantity": user_data["box_quantity"],
        "packaging_id": user_data["packaging_id"],
        "packaging_size": user_data["packaging_size"],
        "tagging": user_data["tagging"],
        "inserts": user_data["inserts"]
    })
    await callback_query.message.answer("Fulfillment setup completed:\n" + ff_data)
    await state.finish()

def register_fulfillment_request(dp: Dispatcher):
    dp.register_callback_query_handler(calculate_fulfillment_start, lambda c: c.data == "calculate_fulfillment")
    dp.register_message_handler(set_product_name, state=FulfillmentForm.product_name)
    dp.register_message_handler(set_quantity, state=FulfillmentForm.quantity)
    dp.register_callback_query_handler(set_marking_type, state=FulfillmentForm.marking_type)
    dp.register_callback_query_handler(set_honest_sign, state=FulfillmentForm.honest_sign)
    dp.register_callback_query_handler(set_box_quantity, state=FulfillmentForm.box_quantity)
    dp.register_callback_query_handler(set_packaging, state=FulfillmentForm.packaging)
    dp.register_callback_query_handler(set_packaging_size, state=FulfillmentForm.packaging_size)
    dp.register_callback_query_handler(set_tagging, state=FulfillmentForm.tagging)
    dp.register_callback_query_handler(set_inserts, state=FulfillmentForm.inserts)
    dp.register_callback_query_handler(set_warehouse, state=FulfillmentForm.warehouse)
