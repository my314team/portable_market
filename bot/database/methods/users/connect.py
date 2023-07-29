import sqlite3


async def connect() -> None:
    db = sqlite3.connect('bot/database/users.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, balance INTEGER, status INTEGER, inner_rating INTEGER, is_banned INTEGER, last_order_time INTEGER)")

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN partner_id INTEGER")
    except:
        pass

    # cursor.execute('UPDATE users SET partner_id="ADMIN"')

    db.commit()

    cursor.close()
    db.close()
