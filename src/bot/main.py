from aiogram import executor


from handlers.fulfillment_handler import register_fulfillment_handlers
from handlers.logistic_handler import register_logistics_handlers
from handlers.catalog_handler import register_catalof_handler
from handlers.base import register_main_commands

from config import dp

register_main_commands(dp=dp)
register_logistics_handlers(dp=dp)
register_fulfillment_handlers(dp=dp)
register_catalof_handler(dp=dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
