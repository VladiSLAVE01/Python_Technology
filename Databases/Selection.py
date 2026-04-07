import sqlite3

database = input()
table = input()

conn = sqlite3.connect(database)
cursor = conn.cursor()

sql = f"SELECT id, name FROM {table} WHERE gender = 'male' AND height > 1.8 ORDER BY name"

cursor.execute(sql)

for id_num, name in cursor.fetchall():
	print(f"{id_num} {name}")

conn.close()