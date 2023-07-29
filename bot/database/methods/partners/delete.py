import sqlite3


async def create(tg_id: int) -> None:
    db = sqlite3.connect('..users.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, balance INTEGER, status INTEGER, inner_rating INTEGER, is_banned INTEGER, last_order_time INTEGER)")

    cursor.commit()
