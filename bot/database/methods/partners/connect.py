import sqlite3


async def connect() -> None:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS partners(partner_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, active INTEGER DEFAULT 0, name TEXT, promocode TEXT, bonus INTEGER DEFAULT 5, total_sales INTEGER DEFAULT 0, total_users INTEGER DEFAULT 0, all_income INTEGER DEFAULT 0, income_left INTEGER DEFAULT 0, project_url TEXT, project_type TEXT)")

    db.commit()

    cursor.close()
    db.close()
