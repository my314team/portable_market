import os
from aiogram import types
from anypay import AnyPayAPI, AnyPayAPIError

from ...database.methods.users import get as user_get
from ...database.methods.goods import get as goods_get
from ...database.methods.orders import get as orders_get
from ...database.methods.orders import update as orders_update

from ...logs import logger
from ...config import get_bot

# Перед использованием проверьте и изучите настройки
# платежной системы
api = AnyPayAPI(
    os.environ["ANYPAY_APP_ID"], os.environ["ANYPAY_KEY"], check=False,
)


async def anypay_create_order(order_id: int, amount_id: int):
    try:
        await api.get_balance()

    except AnyPayAPIError as exc:
        print(exc)

    bill = await api.create_bill(  # easier way to create payment via SCI
        pay_id=order_id,
        amount=amount_id,
        project_id=int(os.environ["ANYPAY_PROJECT_ID"]),
        project_secret=os.environ["ANYPAY_PROJECT_SECRET"],
    )
    return bill.id, bill.url


async def anypay_check_order(pay_id: int) -> bool:
    payments = await api.get_payments(project_id=int(os.environ["ANYPAY_PROJECT_ID"]), pay_id=pay_id)
    is_paid = False

    for payment in payments:
        if payment.status == 'paid':
            is_paid = True
            break

    return is_paid


async def all_unget_orders(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    user_info = await user_get.get(msg.from_user.id)

    if user_info[0] != 1:
        return

    all_orders = await orders_get.get_all()
    not_get_orders = []
    for order in all_orders:
        if order[2] == 1:
            not_get_orders.append(order)

    generated_message = f'⌛️ Список заказов в обработке (всего {len(not_get_orders)}):\n' + '\n\n'.join(
        [f"<b>{order[0]}</b>. Оплачен, в ожидании выдачи товара. \nТовар: {(await goods_get.get(order[6]))[2]}"
         for order in not_get_orders])

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"ап выдать {order[0]}")
        for order in not_get_orders[:10]
    ]
    keyboard.add(*buttons)

    await msg.answer(generated_message, parse_mode="HTML")


async def give_order(msg: types.Message) -> None:
    if msg.from_user is None:
        return

    msg_parts = msg.text.split()

    if len(msg_parts) <= 3:
        await msg.answer(f"Для выдачи товара нужно использовать: {msg.text} <<содержание заказа>>", parse_mode="HTML")
        return

    order_id = int(msg_parts[2])

    order_info = await orders_get.get_info(order_id)

    if order_info is None:
        await msg.answer(f"Заказ (№{order_id}) не найден")
        return

    if order_info[2] == 2:
        await msg.answer(f"Заказ (№{order_id}) уже завершен")
        return

    customer_tg_id = order_info[1]

    order_text = ' '.join(msg_parts[3:])

    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"✅ Заказ получил", callback_data=f"confirmorder_{order_id}"),
        types.InlineKeyboardButton(text=f"❌ Заказ неверен", callback_data=f"badorder_{order_id}")
    ]
    keyboard.add(*buttons)

    await get_bot().send_message(protect_content=True, parse_mode="HTML", chat_id=customer_tg_id, reply_markup=keyboard,
                                 text=f"💡 Новая информация по выдаче заказа (№{order_id})\n\nСодержание: <b>{order_text}</b>\n\nПо любым вопросам обращаться в техническую поддержку. Спасибо за покупку!")

    await msg.answer(f"Сообщение по заказу (№{order_id}) успешно доставлено.", reply_markup=keyboard)


async def confirm_order(clb: types.CallbackQuery):
    if clb.from_user is None:
        return

    msg_parts = clb.data.split('_')

    order_id = int(msg_parts[1])

    order_info = await orders_get.get_info(order_id)

    if order_info is None:
        await clb.answer(f"Заказ (№{order_id}) не найден")
        return

    if order_info[2] == 2:
        await clb.answer(f"Заказ (№{order_id}) уже завершен")
        return

    customer_tg_id = order_info[1]

    if clb.from_user.id != customer_tg_id:
        await clb.answer(f"Вы не являетесь покупателем этого заказа (№{order_id}).")
        return

    await orders_update.update(order_id, "status", 2)
    await clb.message.answer(text=f"🔒 Заказ (№{order_id}) успешно завершен.\nСпасибо за покупку!")
    logger.debug(f"🔒 Заказ (№{order_id}) успешно завершен.")


async def bad_order(clb: types.CallbackQuery):
    if clb.from_user is None:
        return

    msg_parts = clb.data.split('_')

    order_id = int(msg_parts[1])

    order_info = await orders_get.get_info(order_id)

    if order_info is None:
        await clb.answer(f"Заказ (№{order_id}) не найден")
        return

    customer_tg_id = order_info[1]

    if clb.from_user.id != customer_tg_id:
        await clb.answer(f"Вы не являетесь покупателем этого заказа (№{order_id}).")
        return

    await orders_update.update(order_id, "status", 1)
    await clb.message.answer(text=f"🔒 Заказ (№{order_id}) отправлен на уточнение.\nОжидайте ответа.")
    logger.debug(f"🔎 Заказ (№{order_id}) успешно завершен.")
    await get_bot().send_message(protect_content=True, parse_mode="HTML", chat_id=int(os.environ["ADMIN_CHAT_ID"]),
                                 text=f"❗️ Поступило возражение по заказу (№{order_id})!")
