import sqlite3

from . import get


async def update(promocode: str, field_name: str, value) -> None:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        f'UPDATE partners SET {field_name} = {value} WHERE promocode = "{promocode}"')

    db.commit()
    cursor.close()
    db.close()
