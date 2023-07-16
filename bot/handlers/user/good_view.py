from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...database.methods.goods import get as goods_get

from ...logs import logger


async def good_view(clb: types.CallbackQuery) -> None:
    if clb.from_user is None:
        return

    good_info = await goods_get.get(int(clb.data.replace("good_", "")))

    if good_info is None:
        logger.error(f"Товар ({clb.data.replace('good_', '')}) не найден в БД. TG_ID: {clb.from_user.id}.")
        return

    message = f"Товар: <b>{good_info[2]}</b>\nЦена: {good_info[3]}₽\n\n➖ Описание товара: {good_info[10]}\n\n🏷️ Вам осталось лишь оплатить заказ"
    photo = open(f"images/good_{good_info[0]}.png", "rb")

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)

    buttons = [
        types.InlineKeyboardButton(text=f"Оплатить", callback_data=f"create_order_{clb.from_user.id}_{good_info[0]}"),
        types.InlineKeyboardButton(text=f"Проверить оплату", callback_data=f"checkpaygood_{good_info[0]}")

    ]
    keyboard.add(*buttons)

    user_info = await user_get.get(int(clb.from_user.id))

    if user_info is None:
        user_info = await user_create.create(int(clb.from_user.id))
        try:
            logger.debug(
                f"В системе зарегистрирован новый пользователь. TG_ID: {user_info[1]}, USER_ID: {user_info[0]}")
        except KeyError:
            logger.error(
                f"Вероятно, возникла ошибка при регистрации пользователя. TG_ID: {clb.from_user.id}. Информация о пользователе: {user_info}")

    await clb.message.answer_photo(photo, caption=message, parse_mode="HTML", reply_markup=keyboard)
