from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...database.methods.goods import get as goods_get

from ...database.methods.orders import create as orders_create

from ...logs import logger


async def create_order(clb: types.CallbackQuery) -> None:
    if clb.from_user is None:
        return

    order_info = await orders_create.create(int(clb.from_user.id))

    if order_info is None:
        logger.error(
            f"Произошла ошибка при создании заказа (пустой заказ). TG_ID: {clb.from_user.id}. Содержание order_info: {order_info}")
        return

    logger.debug(f"order_info: {order_info}")

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.InlineKeyboardButton(text=f"Оплатить", url="https://t.me/portable_market"),
        types.InlineKeyboardButton(text=f"Проверить оплату", callback_data=f"checkpaygood_{order_info[0]}")

    ]
    keyboard.add(*buttons)

    await clb.message.edit_caption('Нажмите еще раз на кнопку "Оплатить", чтобы перейти к оплате.')
    await clb.message.edit_reply_markup(keyboard)
