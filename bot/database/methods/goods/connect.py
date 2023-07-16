import sqlite3


async def connect() -> None:
    db = sqlite3.connect('bot/database/goods.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS goods(good_id INTEGER PRIMARY KEY AUTOINCREMENT, inner_name TEXT, display_name TEXT, price INTEGER, category_id INTEGER, is_available INTEGER, discount_id INTEGER, sales_cnt INTEGER, created_at INTEGER, modified_at INTEGER, description TEXT)")

    db.commit()

    cursor.close()
    db.close()




