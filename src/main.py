from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from decouple import config

API_TOKEN = config('BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_base_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_calculate = InlineKeyboardButton(text="Рассчитать стоимость", callback_data="calculate")
    keyboard.add(button_calculate)
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = get_base_inline_keyboard()
    await message.reply("Привет! Я бот для расчета стоимости. Нажми на кнопку ниже, чтобы начать.",
                        reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'calculate')
async def ask_for_data(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Отправь мне вес в кг и объем в кубических метрах через пробел (например, '5 0.2').")
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler()
async def calculate_price(message: types.Message):
    try:
        weight, volume = map(float, message.text.split())
        if volume == 0:
            raise ValueError
        density = weight / volume
        price = density * 0.12

        keyboard = get_base_inline_keyboard()

        await message.reply(f"Плотность: {density:.2f} кг/м³\nЦена: ${price:.2f}", reply_markup=keyboard)
    except ValueError:
        await message.reply("Пожалуйста, отправьте вес и объем в правильном формате (например, '5 0.2').")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
