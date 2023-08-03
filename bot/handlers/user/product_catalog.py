from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get
from ...database.methods.goods import get as goods_get

from ...logs import logger


async def product_catalog(msg: types.Message, is_backed: bool = False) -> None:
    if msg.from_user is None:
        return
    message = f"Из какой категории Вы ищете товар?"
    photo = open("images/Категории товаров.png", "rb")

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)


    buttons = [
        types.InlineKeyboardButton(text=f"{c[2]} | {len(await goods_get.get_all_from_category(c[0]))} товаров",
                                   callback_data=f"category_{c[1]}")
        for c in
        (await categories_get.get_all())
    ]
    keyboard.add(*buttons)

    user_info = await user_get.get(int(msg.from_user.id))

    if user_info is None:
        user_info = await user_create.create(int(msg.from_user.id))
        try:
            logger.debug(
                f"В системе зарегистрирован новый пользователь. TG_ID: {user_info[1]}, USER_ID: {user_info[0]}")
        except KeyError:
            logger.error(
                f"Вероятно, возникла ошибка при регистрации пользователя. TG_ID: {msg.from_user.id}. Информация о пользователе: {user_info}")

    if not is_backed:
        await msg.answer_photo(photo=photo, caption=message, parse_mode="HTML", reply_markup=keyboard)
    else:
        await msg.edit_caption(caption=message, parse_mode='HTML', )
        await msg.edit_media(types.InputMedia(media=types.InputFile(f"images/Категории товаров.png")))
        await msg.edit_reply_markup(reply_markup=keyboard)


async def to_categories(clb: types.CallbackQuery):
    if clb.from_user is None:
        return

    await product_catalog(clb.message, is_backed=True)
