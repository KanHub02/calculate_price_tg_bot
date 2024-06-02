from aiogram import executor


from handlers.fulfillment_handler import register_fulfillment_request
from handlers.logistic_handler import register_logistics_handlers
from handlers.base import register_main_commands

from config import dp

register_main_commands(dp=dp)
register_logistics_handlers(dp=dp)
register_fulfillment_request(dp=dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
