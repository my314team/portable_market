from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...database.methods.goods import get as goods_get

from ...logs import logger


async def category_view(clb: types.CallbackQuery) -> None:
    if clb.from_user is None:
        return

    category_info = await categories_get.get(clb.data.replace("category_", ""))

    if category_info is None:
        logger.error(f"Категория товаров ({clb.data.replace('category_', '')}) не найдена. TG_ID: {clb.from_user.id}.")
        return

    message = f"Список доступных товаров в категории <b>{category_info[2]}</b>\n\nНе нашли нужный товар? Предложите нам его добавить, написав в тех. поддержку!"
    photo = open(f"images/{clb.data}.png", "rb")

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"{g[2]} — {g[3]}₽", callback_data=f"good_{g[0]}") for g in
        (await goods_get.get_all())
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

    await clb.message.edit_media(types.InputMedia(media=types.InputFile(f"images/{clb.data}.png")))
    await clb.message.edit_caption(message, parse_mode="HTML")
    await clb.message.edit_reply_markup(keyboard)
