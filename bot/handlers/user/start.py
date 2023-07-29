from aiogram import types
from aiogram.utils.deep_linking import get_start_link, decode_payload

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...logs import logger


async def start(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    command_args = msg.get_args()



    message = f"Добро пожаловать в <b>Portable Market</b>!\n\n❣️ <b>Portable Market</b> - это магазин цифровых товаров прямо в Telegram с низкими ценами, быстрым получением товаров и скоростной поддержкой.\n\n📰 Канал с новостями: @portable_market"
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
        user_info = await user_create.create(int(msg.from_user.id))
        try:
            logger.debug(
                f"В системе зарегистрирован новый пользователь. TG_ID: {user_info[1]}, USER_ID: {user_info[0]}")
        except KeyError:
            logger.error(
                f"Вероятно, возникла ошибка при регистрации пользователя. TG_ID: {msg.from_user.id}. Информация о пользователе: {user_info}")

    await msg.answer_photo(photo, caption=message, parse_mode="HTML", reply_markup=keyboard)
