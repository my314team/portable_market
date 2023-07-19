from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...logs import logger


async def sales(msg: types.Message) -> None:
    if msg.from_user is None:
        return
    message = f"🎉 Акции и скидки - ваши лучшие спутники в мире цифровых товаров! Экономьте больше, получайте больше, наслаждайтесь больше с <b>Portable Market</b>.\n\nСейчас действует скидка <b>-15%</b> на <b>все</b> товары."
    photo = open("images/Акции и скидки.png", "rb")

    await msg.answer_photo(photo=photo, caption=message, parse_mode="HTML")
