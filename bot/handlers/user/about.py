from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...logs import logger


async def about(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    message = """👩‍💻 Разработано by <a href="https://t.me/by_portable">Portable</a>\nИнформация о магазине <a href="http://t.me/portablemarket_bot">Portable Market</a>\n<a href="https://telegra.ph/Polzovatelskoe-soglashenie-07-22-4">Пользовательское соглашение</a>\n\nПо вопросам сотрудничества и работе магазина: @pmarket_support"""

    await msg.answer(text=message, parse_mode="HTML")
