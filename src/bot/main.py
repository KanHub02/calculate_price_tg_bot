from aiogram import executor, types
from aiogram import Dispatcher

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

from config import dp, logging, bot

logging.basicConfig(level=logging.INFO)


async def on_startup(dp: Dispatcher):
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
        ]
    )

    register_main_commands(dp=dp)
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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
