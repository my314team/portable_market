import sqlite3

from . import get


async def create(tg_id: int, partner_id: str, good_id: int) -> list:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f'INSERT INTO orders(customer_tg_id, good_id, partner_id) VALUES ({tg_id}, {good_id}, "{partner_id}")')

    db.commit()
    cursor.close()
    db.close()

    return await get.get(tg_id)
