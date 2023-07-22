import sqlite3

from . import get


async def update(order_id: int, field_name: str, value) -> None:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        f'UPDATE orders SET {field_name} = {value} WHERE order_id = {order_id}')

    db.commit()
    cursor.close()
    db.close()
