import sqlite3

database = input()
table = input()
conn = sqlite3.connect(database)
cursor = conn.cursor()

query = f"SELECT gender, AVG(height), SUM(weight), COUNT(*) FROM {table} GROUP BY gender;"
cursor.execute(query)
result = cursor.fetchall()

for row in result:
    gender, avg_height, total_weight, count = row
    print(f"{gender} {avg_height:.2f} {total_weight}")
