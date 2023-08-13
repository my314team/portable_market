import sqlite3
from typing import Union

from . import get


async def update(good_id: int, field_name: str, value: Union[str, int]) -> None:
    db = sqlite3.connect('bot/database/goods.db')
    cursor = db.cursor()

    if type(value) is int:
        cursor.execute(
            f'UPDATE goods SET "{field_name}" = {value} WHERE "good_id" = {good_id}')
    else:
        cursor.execute(
            f'UPDATE goods SET "{field_name}" = "{value}" WHERE "good_id" = {good_id}')

    db.commit()
    cursor.close()
    db.close()
