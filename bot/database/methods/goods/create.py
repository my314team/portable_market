import sqlite3

from . import get


async def create(inner_name: str, display_name: str) -> list:
    db = sqlite3.connect('bot/database/users.db')
    cursor = db.cursor()

    cursor.execute(
        f"INSERT INTO categories(inner_name, display_name) VALUES ({inner_name}, {display_name})")

    db.commit()
    cursor.close()
    db.close()

    return await get.get(display_name)
