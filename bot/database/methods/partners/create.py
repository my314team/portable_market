import sqlite3

from . import get


async def create(tg_id: int, good_id: int) -> list:
    db = sqlite3.connect('bot/database/partners.db')
    cursor = db.cursor()

    cursor.execute(
        f'INSERT INTO partners(customer_tg_id, good_id) VALUES ({tg_id}, {good_id})')
    #         "CREATE TABLE IF NOT EXISTS partners(partner_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, active INTEGER DEFAULT 0, name TEXT, promocode TEXT, bonus INTEGER DEFAULT 5, total_sales INTEGER DEFAULT 0, total_users INTEGER DEFAULT 0, all_income INTEGER DEFAULT 0, income_left INTEGER DEFAULT 0, project_url TEXT, project_type TEXT)")
    db.commit()
    cursor.close()
    db.close()

    return await get.get(tg_id)
