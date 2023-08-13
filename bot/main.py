from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import handlers
from .database.methods.users import connect as database_users_connect
from .database.methods.categories import connect as database_categories_connect
from .database.methods.goods import connect as database_goods_connect
from .database.methods.orders import connect as database_orders_connect
from .database.methods.partners import connect as database_partners_connect

from .utils.events.daily_sales import sales

from .logs import logger

from .config import get_bot


async def __on_start_up(dp: Dispatcher) -> None:
    await database_users_connect.connect()
    logger.debug("Подключение к БД (users.db) успешно выполнено.")

    await database_categories_connect.connect()
    logger.debug("Подключение к БД (categories.db) успешно выполнено.")

    await database_goods_connect.connect()
    logger.debug("Подключение к БД (goods.db) успешно выполнено.")

    await database_orders_connect.connect()
    logger.debug("Подключение к БД (orders.db) успешно выполнено.")

    await database_partners_connect.connect()
    logger.debug("Подключение к БД (partners.db) успешно выполнено.")


def start_bot():
    dp = Dispatcher(get_bot(), storage=MemoryStorage())

    handlers.setup(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
