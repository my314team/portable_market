from aiogram import types

from ...database.methods.users import get as user_get
from ...database.methods.users import create as user_create

from ...database.methods.partners import get as partners_get

from ...database.methods.orders import get as orders_get

from ...database.methods.goods import get as goods_get

from ...logs import logger


async def stats_menu(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    partner_info = await partners_get.get(msg.from_user.id)

    if partner_info is None:
        return

    message = f"""Здравствуйте, {msg.from_user.full_name}!
Вы находитесь в панели управления партнеров <a href="t.me/portablemarket_bot">Portable Market</a>

🔎 <b>Основная информация</b>
●  Ваш промокод: <code>{partner_info[4].upper()}</code> (нажмите, чтобы скопировать)
●  Пригласительная ссылка: https://t.me/portablemarket_bot?start={partner_info[4].upper()}
●  Привилегии: Скидка {partner_info[5]}% на любой заказ по Вашему промокоду
●  Ссылка на проект: {partner_info[10]}
●  Тип: {partner_info[11]}
    
📊 <b>Статистика продаж</b>
● Кол-во продаж: {partner_info[6]}
Количество покупок, совершенных по Вашему промокоду или пользователями, зарегистрированных по Вашей ссылке
● Новые пользователи: {partner_info[7]}
Количество пользователей, зарегистрированных по Вашей ссылке
● Конверсия продаж: {round(int(partner_info[6]) / max(1, int(partner_info[7])) * 100, 2)}%
Отношение Продаж/Кол-ву пользователей (в %)
    
💰 <b>Финансы</b>
● Средний чек: {round(int(partner_info[8]) / max(1, int(partner_info[6])), 2)}₽
Отношение суммы дохода к кол-ву продаж
● Чистый доход за все время: {partner_info[8]}₽
Сумма в рублях, которая является вашим заработком за все время
● Доступно к выводу: {partner_info[9]}₽
Эту сумму Вы можете вывести, обратившись администратору/куратору"""

    keyboard_structure = [
        [
            types.InlineKeyboardButton(text="Последние продажи", callback_data="lastpartnersales"),
        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_structure)

    await msg.answer(text=message, parse_mode="HTML", reply_markup=keyboard)


async def last_sales(clb: types.CallbackQuery) -> None:
    msg = clb.message
    if msg.from_user is None:
        return

    partner_info = await partners_get.get(int(clb.from_user.id))
    print(partner_info, clb.from_user.id)
    if partner_info is None:
        return

    all_partner_sales = await orders_get.get_by_partner_id(int(partner_info[0]))
    success_partner_sales = []
    for sale in all_partner_sales:
        if sale[2] == 1:
            success_partner_sales.append(sale)

    message = f"""Здравствуйте, {clb.from_user.full_name}!
Вы находитесь в панели управления партнеров <a href="t.me/portablemarket_bot">Portable Market</a>

📨 <b>Последние успешные продажи</b>\n""" + '\n\n'.join(
        [
            f'{order[0]}. {(await goods_get.get(order[6]))[2]}\nЦена: {(await goods_get.get(order[6]))[3]}₽\nЧистый доход: {int((await goods_get.get(order[6]))[11])}₽\nВаша прибыль: {int((await goods_get.get(order[6]))[11] / 2)}₽'
            for order in success_partner_sales] if success_partner_sales else ['оплаченных товары пока нет'])

    print(message)
    keyboard_structure = [
        [
            types.InlineKeyboardButton(text="Последние продажи", callback_data="lastpartnersales"),
        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_structure)

    await clb.message.answer(text=message, parse_mode="HTML")
