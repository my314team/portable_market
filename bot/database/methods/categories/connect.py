import sqlite3


async def connect() -> None:
    db = sqlite3.connect('bot/database/categories.db')
    cursor = db.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS categories(category_id INTEGER PRIMARY KEY AUTOINCREMENT, inner_name TEXT, display_name TEXT)")

    db.commit()

    cursor.close()
    db.close()




