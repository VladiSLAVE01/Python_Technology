import sqlite3

database = input()
table = input()
mark_table = input()


import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect(database)
cursor = conn.cursor()

# Выполняем запрос
query = f"""
SELECT 
    s.name,
    ROUND(AVG(m.mark)) AS average_mark
FROM {table} s
JOIN {mark_table} m ON s.id = m.id
GROUP BY s.id, s.name;
"""
cursor.execute(query)

# Получаем результат
result = cursor.fetchall()

# Выводим результат

for name, avg_mark in result:
    print(f"{name} {avg_mark}")  # Преобразуем в целое число и выводим
