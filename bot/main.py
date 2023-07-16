from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import handlers
from .database.methods.users import connect as database_users_connect
from .database.methods.categories import connect as database_categories_connect
from .database.methods.goods import connect as database_goods_connect
from .logs import logger


async def __on_start_up(dp: Dispatcher) -> None:
    await database_users_connect.connect()
    logger.debug("Подключение к БД (users.db) успешно выполнено.")

    await database_categories_connect.connect()
    logger.debug("Подключение к БД (categories.db) успешно выполнено.")

    await database_goods_connect.connect()
    logger.debug("Подключение к БД (goods.db) успешно выполнено.")

def start_bot():
    bot = Bot(token="6327425346:AAHg1xh_YxInLPyQmYfrzrPQZ0Q-ATrtAyk")
    dp = Dispatcher(bot, storage=MemoryStorage())

    handlers.setup(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
