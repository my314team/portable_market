from aiogram import types
from aiogram.utils.exceptions import MessageNotModified

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
    try:
        photo = open(f"images/{clb.data}.png", "rb")
    except FileNotFoundError:
        logger.error(f"Не найдено изображение товара {clb.data} (images/{clb.data}.png).")
        photo = ""

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"{g[2]} | {g[3]}₽", callback_data=f"good_{g[0]}") for g in
        (await goods_get.get_all_from_category(category_info[0]))
    ]
    buttons = buttons[:9]
    buttons.append(
        types.InlineKeyboardButton(text=f"◀️ Назад", callback_data="to_categories")
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

    await clb.message.edit_media(types.InputMedia(media=types.InputFile(f"images/{clb.data}.png")))
    await clb.message.edit_caption(message, parse_mode="HTML")
    try:
        await clb.message.edit_reply_markup(keyboard)
    except MessageNotModified:
        pass
