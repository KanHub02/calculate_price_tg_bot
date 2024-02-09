from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

import statics
import utils



API_TOKEN = config("BOT_TOKEN")
MANAGER_CHAT_ID = config("MANAGER_CHAT_ID")
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    phone_number = State()
    cargo_type = State()
    title = State()
    weight = State()
    volume = State()


def get_base_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="Рассчитать стоимость логистики", callback_data="calculate_logistics"
        ),
        InlineKeyboardButton(text="Как пользоваться ботом", callback_data="how_to_use"),
        InlineKeyboardButton(text="Менеджер", callback_data="manager"),
    ]
    keyboard.add(*buttons)
    return keyboard


def select_type():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="Тнп", callback_data="cargo_tnp"),
        InlineKeyboardButton(text="Текстиль", callback_data="cargo_textile"),
    ]
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message):
    keyboard = get_base_inline_keyboard()
    await bot.send_message(
        message.chat.id,
        "Привет! Я бот для расчета стоимости логистики. Выбери действия, используя кнопки ниже.",
        reply_markup=keyboard,
    )
    await Form.cargo_type.set()


@dp.callback_query_handler(
    lambda c: c.data in ["cargo_tnp", "cargo_textile"], state=Form.cargo_type
)
@dp.callback_query_handler(
    lambda c: c.data in ["cargo_tnp", "cargo_textile"], state=Form.cargo_type
)
async def set_cargo_type(callback_query: types.CallbackQuery, state: FSMContext):
    cargo_type_map = {"cargo_tnp": "Тнп", "cargo_textile": "Текстиль"}
    await state.update_data(cargo_type=cargo_type_map.get(callback_query.data))
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
    await message.reply("Отправьте вес груза в кг.")


@dp.message_handler(state=Form.weight)
async def set_weight(message: types.Message, state: FSMContext):
    corrected_input = message.text.replace(",", ".")
    if not corrected_input.replace(".", "", 1).isdigit():
        await message.reply(
            "Пожалуйста, введите вес в килограммах числом. Например, 10.5 или 20. Попробуйте еще раз."
        )
        return  

    await state.update_data(weight=corrected_input)
    await Form.volume.set()
    await message.reply("Теперь отправьте объем груза в кубических метрах.")


@dp.message_handler(state=Form.volume)
async def set_volume(message: types.Message, state: FSMContext):        
    corrected_input = message.text.replace(",", ".")
    print(corrected_input)
    if not corrected_input.replace(".", "", 1).isdigit():
        await message.reply(
            "Пожалуйста, введите объем кубическими метрами числом. Например, 1.5 или 2. Попробуйте еще раз."
        )

    await state.update_data(volume=corrected_input)
    user_data = await state.get_data()
    cargo_type = user_data["cargo_type"]
    title = user_data["title"]
    weight = user_data["weight"]
    volume = user_data["volume"]
    density = float(weight) / float(volume)

    match user_data["cargo_type"]:
        case "Тнп":
            logistic_price__express = statics.calculate_price_per_kg_for_tnp_express(density)
            logistic_price__standart = statics.calculate_price_per_kg_for_tnp_standart(density)

        case "Текстиль":
            logistic_price__express = statics.calculate_price_per_kg_for_textile_express(
                density
            )
            logistic_price__standart = statics.calculate_price_per_kg_for_textile_standart(
                density
            )
    
    rounded_weight = round(float(weight), 2)
    rounded_volume = round(float(volume), 2)
    logistic_price__express = logistic_price__express if isinstance(logistic_price__express, str) else round(logistic_price__express, 2)
    logistic_price__standart = logistic_price__standart if isinstance(logistic_price__standart, str) else round(logistic_price__standart, 2) 
    answer_message = f"Товар: {title}\nВид груза: {cargo_type}\nВес: {rounded_weight} кг\nОбъем: {rounded_volume} куб.м\nПлотность груза: {density:.2f}\nЦена Express: {logistic_price__express}\nЦена Standart: {logistic_price__standart}."
    await message.reply(
        answer_message
    )
    await bot.send_message(
        message.chat.id,
        "Расчет выполнен. Используйте /start, чтобы выполнить новый расчет или получить другую информацию.",
        reply_markup=get_base_inline_keyboard(),
    )
    phone_number = user_data["phone_number"]
    await state.finish()
    manager_message = f"@{message.from_user.username} отправил заявку:\n" +  f"Номер телефона:{phone_number}\n" + answer_message
    await utils.send_message(API_TOKEN, MANAGER_CHAT_ID, manager_message)


@dp.callback_query_handler(lambda c: c.data == "calculate_logistics", state="*")
async def calculate_logistics(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = (
        select_type()
    )  # Вызываем функцию для получения клавиатуры с выбором типа груза
    await bot.send_message(
        callback_query.from_user.id, "Выберите тип груза:", reply_markup=keyboard
    )
    await Form.cargo_type.set()  # Устанавливаем состояние для выбора типа груза
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "how_to_use", state="*")
async def how_to_use(callback_query: types.CallbackQuery):
    instructions = "Чтобы начать работу с ботом, выберите один из предложенных вариантов на клавиатуре. Для расчета стоимости логистики следуйте подсказкам."
    await bot.send_message(callback_query.from_user.id, instructions)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "manager", state="*")
async def contact_manager(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "Для связи с менеджером используйте контакт: @ummanagerch",
    )
    await bot.answer_callback_query(callback_query.id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
