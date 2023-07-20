import sqlite3
from typing import Union


async def get(good_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/goods.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM goods WHERE good_id={good_id}')

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


async def get_all() -> Union[None, list]:
    db = sqlite3.connect('bot/database/goods.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM goods")

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result


async def get_all_from_category(category_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/goods.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM goods WHERE category_id={category_id}")

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result
