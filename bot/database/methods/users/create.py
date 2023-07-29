import sqlite3

from . import get


async def create(tg_id: int, promocode: str = 'ADMIN') -> list:
    db = sqlite3.connect('bot/database/users.db')
    cursor = db.cursor()

    cursor.execute(
        f'INSERT INTO users(tg_id, balance, status, inner_rating, is_banned, last_order_time, partner_id) VALUES ({tg_id}, 0, 1, 5, 0, 0, "{promocode}")')


    db.commit()
    cursor.close()
    db.close()

    return await get.get(tg_id)
