import sqlite3
from typing import Union


async def get(tg_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM orders WHERE customer_tg_id={tg_id}')

    result = cursor.fetchall()[-1]

    cursor.close()
    db.close()

    return result


async def get_info(order_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM orders WHERE order_id={order_id}')

    result = cursor.fetchall()[-1]

    cursor.close()
    db.close()

    return result


async def get_all() -> Union[None, list]:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM orders")

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result


async def get_by_partner_id(partner_id: str) -> Union[None, list]:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM orders WHERE partner_id="{partner_id.upper()}"')

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result
