from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

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

    # message = f"Товар: <b>{good_info[2]}</b>\nЦена: {good_info[3] * (1 - (await partners_get.get_by_promo((await user_get.get(clb.from_user.id))[7]))[5] / 100)} <s>{good_info[3]}</s>₽\n\n➖ Описание товара: {good_info[10]}\n\n🏷️ Вам осталось лишь оплатить заказ"
    # Со скидкой партнера, временно убрано

    message = f"Товар: <b>{good_info[2]}</b>\nЦена: {good_info[3] - good_info[6]} <s>{good_info[3]}</s>₽\n\n➖ Описание товара: {good_info[10]}\n\n🏷️ Вам осталось лишь оплатить заказ"

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        types.InlineKeyboardButton(text=f"Оплатить", callback_data=f"create_order_{clb.from_user.id}_{good_info[0]}"),
        types.InlineKeyboardButton(text=f"Проверить оплату", callback_data=f"checkpaygood_{good_info[0]}")

    ]
    buttons = buttons[:9]
    buttons.append(
        types.InlineKeyboardButton(text=f"◀️ Назад",
                                   callback_data=f"category_{(await categories_get.get_all())[good_info[4] - 1][1]}")
    )
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

    await clb.message.edit_media(types.InputMedia(media=types.InputFile(f"images/good_{good_info[0]}.png")))
    await clb.message.edit_caption(message, parse_mode="HTML")
    try:
        await clb.message.edit_reply_markup(keyboard)
    except MessageNotModified:
        pass
