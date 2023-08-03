import sqlite3
from typing import Union


async def get(inner_name: str) -> Union[None, list]:
    db = sqlite3.connect('bot/database/categories.db')
    cursor = db.cursor()

    cursor.execute(
        f'SELECT * FROM categories WHERE inner_name="{inner_name}"')

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


async def get_all() -> Union[None, list]:
    db = sqlite3.connect('bot/database/categories.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM categories")

    result = cursor.fetchall()

    cursor.close()
    db.close()
    return result
