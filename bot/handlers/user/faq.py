from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.categories import get as categories_get

from ...logs import logger


async def faq(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    message = [("Как совершить покупку?", "Необходимо перейти в диалог с ботом @portablemarket_bot и ввести /start, далее следовать инструкции.", "how_to_order"),

    ("Не могу найти нужный товар.", "Если вы не можете найти товар там, где он обычно находится, вероятно, он временно недоступен для покупки. Попробуйте зайти в каталог чуть позже.", "good_not_found"),

    ("Как применить промокод?", "При совершении покупки, на последнем этапе, у вас появится кнопка для ввода промокода. Если он у нас имеется, то нажмите на нее и следуйте дальнейшим указаниям.", "how_to_use_promo"),

    ("Не работает оплата.", "Если выдает ошибку на странице совершения платежа:\nПосмотрите, есть ли в новостном канале магазина информация о возможном сбое. В случае если таковой имеется подождите немного. Напишите в техническую поддержку, чтобы в ускоренном режиме решить проблему.", "payment_not_work"),

    ("Оплатил товар, но бот не видит платеж.", "Проверьте платежную историю. Если там отображается, что платеж прошел, то подождите 5-10 минут. Если проблема все еще осталась, обратитесь в техническую поддержку.", "no_money_sent"),

    ("Не работает бот.", "Если бот не отвечает на сообщения больше 1 минуты, то, вероятно, он проводится техническое обслуживание. В этом случае рекомендуем следить за статусом работы в новостном канале магазина.", "bot_off")

    ]

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"{q_a[0]}", callback_data=f"qa_{q_a[2]}") for q_a in
        message
    ]
    keyboard.add(*buttons)

    photo = open("images/Вопрос-Ответ.png", "rb")

    await msg.answer_photo(photo=photo, caption="📚 Не знаете, как сделать заказ или у вас есть вопросы? Посетите раздел Вопрос-Ответ и найдите ответы прямо здесь!\n(Используйте кнопки для удобного взаимодействия)", parse_mode="HTML", reply_markup=keyboard)
