import sqlite3
from typing import Union


async def get(tg_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM partners WHERE tg_id={tg_id}')

    try:
        result = cursor.fetchall()[-1]
    except IndexError:
        return

    cursor.close()
    db.close()

    return result

async def get_by_promo(promocode: str) -> Union[None, list]:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM partners WHERE promocode="{promocode}"')

    try:
        result = cursor.fetchall()[-1]
    except IndexError:
        return

    cursor.close()
    db.close()

    return result


async def get_all() -> Union[None, list]:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM partners")

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result
