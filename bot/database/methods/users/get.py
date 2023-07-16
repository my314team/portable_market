import sqlite3
from typing import Union


async def get(tg_id: int) -> Union[None, list]:
    db = sqlite3.connect('bot/database/users.db')
    cursor = db.cursor()

    cursor.execute(
        f"SELECT * FROM users WHERE tg_id={tg_id}")

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result
