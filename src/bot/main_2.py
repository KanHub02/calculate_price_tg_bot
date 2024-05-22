from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

from api import *


API_TOKEN = config("BOT_TOKEN")
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class LogisticsForm(StatesGroup):
    phone_number = State()
    cargo_type = State()
    packaging_type = State()
    title = State()
    weight = State()
    volume = State()
    quantity = State()
    insurance_cost = State()


class FulfillmentForm(StatesGroup):
    product_name = State()
    quantity = State()
    marking_type = State()  # Добавлено состояние для выбора типа маркировки
    honest_sign = State()
    packaging = State()
    packaging_size = State()
    tagging = State()
    inserts = State()
    box_quantity = State()
    warehouse = State()


def select_packaging_type(packaging_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=packaging["title"], callback_data=f"packaging_{packaging['id']}"
        )
        for packaging in packaging_types
    ]
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
    keyboard.add(*buttons)
    return keyboard


def select_type(cargo_types):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=cargo_type["title"], callback_data=f"cargo_{cargo_type['id']}"
        )
        for cargo_type in cargo_types
    ]
    keyboard.add(*buttons)
    return keyboard


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


def yes_no_keyboard():
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
    no_button = InlineKeyboardButton(text="Нет", callback_data="no")
    keyboard.add(yes_button, no_button)
    return keyboard


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message):
    keyboard = main_menu_keyboard()
    await message.answer(
        "Добро пожаловать! Пожалуйста, выберите действие:", reply_markup=keyboard
    )
    data = {
        "tg_id": message.from_user.id,
        "tg_username": message.from_user.username,
    }
    await create_tg_user(data)


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text="Рассчитать Логистику", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(
            text="Рассчитать Фулфилмент", callback_data="calculate_fulfillment"
        ),
        InlineKeyboardButton(text="Курс перевода", callback_data="exchange_rate"),
        InlineKeyboardButton(text="Полезности", callback_data="utilities"),
        InlineKeyboardButton(text="Менеджер", callback_data="manager"),
        InlineKeyboardButton(text="Условия работы", callback_data="work_conditions"),
        InlineKeyboardButton(text="Стать Партнером", callback_data="become_partner"),
        InlineKeyboardButton(
            text="Как пользоваться ботом?", callback_data="how_to_use"
        ),
    ]
    keyboard.add(*buttons)
    return keyboard


@dp.callback_query_handler(lambda c: c.data == "calculate_logistics")
async def calculate_logistics_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    cargo_types = await fetch_cargo_types()
    keyboard = select_type(cargo_types)
    await bot.send_message(
        callback_query.from_user.id, "Выберите тип груза:", reply_markup=keyboard
    )
    await LogisticsForm.cargo_type.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("cargo_"), state=LogisticsForm.cargo_type
)
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
    await LogisticsForm.packaging_type.set()
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(
    lambda c: c.data.startswith("packaging_"), state=LogisticsForm.packaging_type
)
async def set_packaging_type(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    packaging_types = await fetch_packaging_types()
    packaging_type = next(
        (pt for pt in packaging_types if pt["id"] == packaging_id), None
    )
    if packaging_type:
        await state.update_data(
            packaging_type_id=packaging_id, packaging_type=packaging_type["title"]
        )
    await LogisticsForm.phone_number.set()
    await bot.send_message(callback_query.from_user.id, "Введите номер телефона.")
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=LogisticsForm.phone_number)
async def set_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await LogisticsForm.title.set()
    await message.reply("Введите название товара.")


@dp.message_handler(state=LogisticsForm.title)
async def set_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await LogisticsForm.weight.set()
    await message.reply("Введите вес груза в кг.")


@dp.message_handler(state=LogisticsForm.weight)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await LogisticsForm.volume.set()
    await message.reply("Введите объем груза в кубических метрах.")


@dp.message_handler(state=LogisticsForm.volume)
async def set_volume(message: types.Message, state: FSMContext):
    await state.update_data(volume=message.text)
    await LogisticsForm.quantity.set()  # переход к запросу количества товара
    await message.reply("Введите количество товара.")


@dp.message_handler(state=LogisticsForm.quantity)
async def set_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await LogisticsForm.insurance_cost.set()  # переход к запросу стоимости товара для страховки
    await message.reply("Введите стоимость товара для расчета страховки.")


@dp.message_handler(state=LogisticsForm.insurance_cost)
async def set_insurance_cost(message: types.Message, state: FSMContext):
    await state.update_data(insurance_cost=message.text)
    user_data = await state.get_data()

    # Создаем POST-запрос к вашему API
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
    await message.reply(f"Запрос на логистику создан. Статус: {api_response}")
    keyboard = main_menu_keyboard()
    await message.reply("Выберите действие:", reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "calculate_fulfillment")
async def calculate_fulfillment_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите наименование товара:")
    await FulfillmentForm.product_name.set()


@dp.message_handler(state=FulfillmentForm.product_name)
async def set_product_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.reply("Введите количество товара:")
    await FulfillmentForm.quantity.set()


@dp.message_handler(state=FulfillmentForm.quantity)
async def ask_marking_type(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    marking_types = (
        await fetch_marking_types()
    )  # Предполагаем, что у вас есть такая функция
    keyboard = select_marking_type(marking_types)
    await message.reply("Выберите тип маркировки:", reply_markup=keyboard)
    await FulfillmentForm.marking_type.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("marking_"), state=FulfillmentForm.marking_type
)
async def set_marking_type(callback_query: types.CallbackQuery, state: FSMContext):
    marking_id = callback_query.data.split("_")[1]
    await state.update_data(marking_type_id=marking_id)
    await callback_query.answer("Тип маркировки выбран.")
    await ask_box_quantity(callback_query.message, state)  # Переходим к следующему шагу


async def ask_box_quantity(message: types.Message, state: FSMContext):
    await message.reply("Сколько помещается штук в короб 60x40x40?")
    await FulfillmentForm.box_quantity.set()


@dp.message_handler(state=FulfillmentForm.box_quantity)
async def set_box_quantity(message: types.Message, state: FSMContext):
    await state.update_data(box_quantity=message.text)
    packaging_options = await fetch_packaging_options()
    keyboard = select_packaging_option(packaging_options)
    await message.reply("Выберите вид упаковки и размер:", reply_markup=keyboard)
    await FulfillmentForm.packaging.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("packaging_"), state=FulfillmentForm.packaging
)
async def set_packaging(callback_query: types.CallbackQuery, state: FSMContext):
    packaging_id = callback_query.data.split("_")[1]
    sizes = await fetch_packaging_sizes(packaging_id)
    keyboard = select_packaging_sizes(sizes)
    await bot.send_message(
        callback_query.from_user.id, "Выберите размер упаковки:", reply_markup=keyboard
    )
    await FulfillmentForm.packaging_size.set()
    await state.update_data(packaging_id=packaging_id)  # Сохраняем ID упаковки
    await callback_query.answer()  # Ответить на колбэк-запрос, чтобы убрать индикатор загрузки


@dp.callback_query_handler(
    lambda c: c.data.startswith("size_"), state=FulfillmentForm.packaging_size
)
async def set_packaging_size(callback_query: types.CallbackQuery, state: FSMContext):
    size = callback_query.data.split("_")[1]
    await state.update_data(packaging_size=size)
    keyboard = yes_no_keyboard()  # Клавиатура для вопроса про биркование
    await bot.send_message(
        callback_query.from_user.id, "Нужно ли биркование?", reply_markup=keyboard
    )
    await FulfillmentForm.tagging.set()


@dp.callback_query_handler(
    lambda c: c.data in ["yes", "no"], state=FulfillmentForm.tagging
)
async def set_tagging(callback_query: types.CallbackQuery, state: FSMContext):
    tagging = callback_query.data == "yes"
    await state.update_data(tagging=tagging)
    keyboard = yes_no_keyboard()  # Клавиатура для вопроса про вложения
    await callback_query.message.reply("Нужны ли вложения?", reply_markup=keyboard)
    await FulfillmentForm.inserts.set()


@dp.callback_query_handler(
    lambda c: c.data in ["yes", "no"], state=FulfillmentForm.inserts
)
async def set_inserts(callback_query: types.CallbackQuery, state: FSMContext):
    inserts = callback_query.data == "yes"
    await state.update_data(inserts=inserts)
    # Теперь вызываем функцию для запроса склада
    warehouses = (
        await fetch_warehouses()
    )  # Замените этой функцией вызов API для получения списка складов
    keyboard = select_warehouse_keyboard(warehouses)
    await bot.send_message(
        callback_query.from_user.id, "Выберите склад:", reply_markup=keyboard
    )
    await FulfillmentForm.warehouse.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("warehouse_"), state=FulfillmentForm.warehouse
)
async def set_warehouse(callback_query: types.CallbackQuery, state: FSMContext):
    warehouse_id = callback_query.data.split("_")[1]
    await state.update_data(warehouse_id=warehouse_id)
    user_data = await state.get_data()
    print(user_data)
    yes_or_no_map = {"Да": True, "Нет": False}
    # Создаем POST-запрос к вашему API
    api_data = {
        "tg_client_id": callback_query.from_user.id,
        "marking_type_id": user_data["marking_type_id"],
        "package_id": user_data["packaging_id"],
        "packaging_size": user_data["packaging_size"],
        "stock_id": user_data["warehouse_id"],
        "product_title": user_data["product_name"],
        "quantity": user_data["quantity"],
        "need_attachment": yes_or_no_map.get(user_data["inserts"]),
        "need_taging": yes_or_no_map.get(user_data["tagging"]),
        "count_of_boxes": user_data["box_quantity"],
    }
    api_response = await create_fulfillment_request(api_data)
    await callback_query.answer(f"Запрос на фулфиллмент создан. Статус: {api_response}")
    keyboard = main_menu_keyboard()
    await callback_query.answer("Выберите действие:", reply_markup=keyboard)
    await state.finish()


# @dp.message_handler(state=FulfillmentForm.honest_sign)
# async def set_honest_sign(message: types.Message, state: FSMContext):
#     honest_sign = message.text.lower() == "да"
#     await state.update_data(honest_sign=honest_sign)
#     packaging_options = await fetch_packaging_options()
#     keyboard = select_packaging_option(packaging_options)
#     await message.reply("Выберите вид упаковки и размер:", reply_markup=keyboard)
#     await FulfillmentForm.packaging.set()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
