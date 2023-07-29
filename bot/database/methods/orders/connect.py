import sqlite3


async def connect() -> None:
    db = sqlite3.connect('bot/database/orders.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orders(order_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_tg_id INTEGER, status INTEGER DEFAULT 0, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, finished_at DATETIME, manager_comment TEXT, good_id INTEGER)")

    try:
        cursor.execute('ALTER TABLE orders ADD COLUMN partner_id TEXT DEFAULT "ADMIN"')
    except:
        pass


    db.commit()

    cursor.close()
    db.close()
