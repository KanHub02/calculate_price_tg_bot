from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
import aiohttp

API_TOKEN = config("BOT_TOKEN")
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    phone_number = State()
    cargo_type = State()
    packaging_type = State()
    title = State()
    weight = State()
    volume = State()
    quantity = State()
    insurance_cost = State()

async def create_tg_user(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-telegram-user/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"

async def fetch_cargo_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-cargo-types/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_packaging_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-cargo-packages/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def select_type(cargo_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=cargo_type["title"], callback_data=f"cargo_{cargo_type['id']}")
        for cargo_type in cargo_types
    ]
    keyboard.add(*buttons)
    return keyboard

def select_packaging(packaging_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=packaging["title"], callback_data=f"packaging_{packaging['id']}")
        for packaging in packaging_types
    ]
    keyboard.add(*buttons)
    return keyboard

async def create_logistic_request(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-logistic-request/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"

def menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Вызвать менеджера", callback_data="call_manager"),
        InlineKeyboardButton(text="Просчитать другой товар", callback_data="calculate_another"),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    ]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message):
    cargo_types = await fetch_cargo_types()
    keyboard = select_type(cargo_types)
    await bot.send_message(
        message.chat.id, "Выберите тип груза:", reply_markup=keyboard
    )
    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
    }
    await create_tg_user(data)
    await Form.cargo_type.set()

@dp.callback_query_handler(lambda c: c.data.startswith("cargo_"), state=Form.cargo_type)
async def set_cargo_type(callback_query: types.CallbackQuery, state: FSMContext):
    cargo_id = callback_query.data.split("_")[1]
    cargo_types = await fetch_cargo_types()
    cargo_type = next((ct for ct in cargo_types if ct["id"] == cargo_id), None)
    if cargo_type:
        await state.update_data(cargo_type_id=cargo_id, cargo_type=cargo_type["title"])

    packaging_types = await fetch_packaging_types()
    keyboard = select_packaging(packaging_types)
    await bot.send_message(
        callback_query.from_user.id, "Выберите вид упаковки:", reply_markup=keyboard
    )
    await Form.packaging_type.set()
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("packaging_"), state=Form.packaging_type)
async def set_packaging_type(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    packaging_types = await fetch_packaging_types()
    packaging_type = next((pt for pt in packaging_types if pt["id"] == packaging_id), None)
    if packaging_type:
        await state.update_data(packaging_type_id=packaging_id, packaging_type=packaging_type["title"])
    await Form.phone_number.set()
    await bot.send_message(callback_query.from_user.id, "Введите номер телефона.")
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=Form.phone_number)
async def set_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await Form.title.set()
    await message.reply("Введите название товара.")

@dp.message_handler(state=Form.title)
async def set_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await Form.weight.set()
    await message.reply("Введите вес груза в кг.")

@dp.message_handler(state=Form.weight)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await Form.volume.set()
    await message.reply("Введите объем груза в кубических метрах.")

@dp.message_handler(state=Form.volume)
async def set_volume(message: types.Message, state: FSMContext):
    await state.update_data(volume=message.text)
    await Form.quantity.set()  # переход к запросу количества товара
    await message.reply("Введите количество товара.")

@dp.message_handler(state=Form.quantity)
async def set_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await Form.insurance_cost.set()  # переход к запросу стоимости товара для страховки
    await message.reply("Введите стоимость товара для расчета страховки.")

@dp.message_handler(state=Form.insurance_cost)
async def set_insurance_cost(message: types.Message, state: FSMContext):
    await state.update_data(insurance_cost=message.text)
    user_data = await state.get_data()

    # Создаем POST-запрос к вашему API
    api_data = {
        "tg_client_id": message.from_user.id,
        "cargo_type_id": user_data["cargo_type_id"],
        "cargo_package_type_id": user_data["packaging_type_id"],
        "weight": float(user_data["weight"]),
        "quantity": int(user_data["quantity"]),
        "volume": float(user_data["volume"]),
        "insurance_cost": float(user_data["insurance_cost"]),
    }
    api_response = await create_logistic_request(api_data)
    await message.reply(f"Запрос на логистику создан. Статус: {api_response}")
    keyboard = menu_keyboard()
    await message.reply("Выберите действие:", reply_markup=keyboard)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "call_manager")
async def call_manager(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Менеджер скоро с вами свяжется!")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == "calculate_another")
async def calculate_another(callback_query: types.CallbackQuery):
    cargo_types = await fetch_cargo_types()
    keyboard = select_type(cargo_types)
    await bot.send_message(callback_query.from_user.id, "Выберите тип груза:", reply_markup=keyboard)
    await Form.cargo_type.set()
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def main_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Добро пожаловать в главное меню!")
    await bot.answer_callback_query(callback_query.id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
