import sqlite3

db = sqlite3.connect('bot/database/orders.db')
cursor = db.cursor()

cursor.execute(
    f'SELECT * FROM orders WHERE customer_tg_id=1582664686')

result = cursor.fetchall()[-1]

cursor.close()
db.close()

print(result)