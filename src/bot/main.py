from aiogram import executor, types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.fulfillment_handler import register_fulfillment_handlers
from handlers.logistic_handler import register_logistics_handlers
from handlers.catalog_handler import register_catalog_handler
from handlers.base import register_main_commands
from handlers.article_handler import register_articles_handlers
from handlers.rest_other_handler import register_rest_other_handler
from handlers.feedback_usefull_handler import register_feedback_handlers
from handlers.translation_course_handler import register_course_handler
from handlers.translation_info_handler import register_translation_handler
from handlers.scammers_handler import register_scammers_handler
from handlers.review_form_handler import register_review_handlers
from handlers.how_to_use_handler import register_how_to_use_handler
from handlers.partner_lead_handler import register_partner_lead_info_handler
from handlers.working_condition_handler import register_working_condition_handler

from config import dp, logging, bot

logging.basicConfig(level=logging.INFO)

async def super_command_handler(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Да", callback_data="confirm_super_yes"),
        InlineKeyboardButton(text="Нет", callback_data="confirm_super_no")
    ]
    keyboard.add(*buttons)
    await message.answer("Вы уверены, что хотите перезапустить все состояния и очистить чат?", reply_markup=keyboard)

async def confirm_super_yes_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    chat_id = callback_query.message.chat.id

    N = 100
    last_message_id = callback_query.message.message_id
    for i in range(N):
        try:
            await bot.delete_message(chat_id, last_message_id - i)
        except Exception as e:
            i += 1
            logging.error(f"Ошибка при удалении сообщения {last_message_id - i}: {e}")
            break


async def confirm_super_no_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Отменено.")
    await callback_query.answer()

async def on_startup(dp: Dispatcher):
    await bot.set_my_commands(
        [
            BotCommand("start", "Запустить бота"),
            BotCommand("super", "Перезапустить все состояния и очистить чат")
        ]
    )

    register_main_commands(dp=dp)
    dp.register_message_handler(super_command_handler, Command("super"), state="*")
    dp.register_callback_query_handler(confirm_super_yes_handler, lambda c: c.data == "confirm_super_yes", state="*")
    dp.register_callback_query_handler(confirm_super_no_handler, lambda c: c.data == "confirm_super_no", state="*")
    register_logistics_handlers(dp=dp)
    register_fulfillment_handlers(dp=dp)
    register_catalog_handler(dp=dp)
    register_articles_handlers(dp=dp)
    register_rest_other_handler(dp=dp)
    register_feedback_handlers(dp=dp)
    register_course_handler(dp=dp)
    register_translation_handler(dp=dp)
    register_scammers_handler(dp=dp)
    register_review_handlers(dp=dp)
    register_partner_lead_info_handler(dp=dp)
    register_how_to_use_handler(dp=dp)
    register_working_condition_handler(dp=dp)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
