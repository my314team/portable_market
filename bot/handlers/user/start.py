from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.partners import update as partners_update
from ...database.methods.partners import get as partners_get

from ...logs import logger

from ... import config


async def start(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    command_args = msg.get_args()

    message = f'Добро пожаловать в <b>{config.SHOP_NAME}</b>!\n\n❣️ <b>{config.SHOP_NAME}</b> - это магазин цифровых товаров прямо в Telegram с низкими ценами, быстрым получением товаров и скоростной поддержкой.\n\n📰 <a href="{config.SHOP_NEWS_CHANNEL_URL}">Канал с новостями</a>'
    photo = open("images/Стартовая картинка.png", "rb")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton(text="Каталог товаров 🛒"),
        types.KeyboardButton(text="Отзывы клиентов 📪"),
        types.KeyboardButton(text="Поддержка 📝"),
        types.KeyboardButton(text="Вопрос-Ответ 🔍"),
        types.KeyboardButton(text="О магазине"),
    ]
    keyboard.add(*buttons)

    user_info = await user_get.get(int(msg.from_user.id))

    if user_info is None:
        user_info = await user_create.create(int(msg.from_user.id), promocode=command_args if command_args else 'ADMIN')
        if command_args:
            try:
                await partners_update.update(command_args, "total_users",
                                             (await partners_get.get_by_promo(command_args))[7] + 1)
            except Exception as ERROR:
                logger.error(f"Ошибка при добавлении пользователя к партнеру: {ERROR}")
        try:
            logger.debug(
                f"В системе зарегистрирован новый пользователь. TG_ID: {user_info[1]}, USER_ID: {user_info[0]}")
        except KeyError:
            logger.error(
                f"Вероятно, возникла ошибка при регистрации пользователя. TG_ID: {msg.from_user.id}. Информация о пользователе: {user_info}")

    await msg.answer_photo(photo, caption=message, parse_mode="HTML", reply_markup=keyboard)
