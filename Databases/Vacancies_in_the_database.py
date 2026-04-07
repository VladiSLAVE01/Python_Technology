import csv
import sqlite3
import pandas as pd

database_name = input().strip()
csv_file = input().strip()
table_name = input().strip()
currency_table = input().strip()

# Создаем соединение с базой данных
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Загружаем курсы валют
# Да, в задачу просят обращаться к бд, но я не смог сообразить как этой сделать
cursor.execute(f"SELECT * FROM {currency_table}")
currency_rates = {}
for row in cursor.fetchall():
	date_key = row[0]
	currency_rates[date_key] = {
		'BYR': row[1], 'USD': row[2], 'EUR': row[3], 'KZT': row[4],
		'UAH': row[5], 'AZN': row[6], 'KGS': row[7], 'UZS': row[8]
	}

# Создаем таблицу для результатов
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        name TEXT,
        salary INTEGER,
        area_name TEXT,
        published_at TEXT
    )
""")
cursor.execute(f"DELETE FROM {table_name}")

# Читаем и обрабатываем данные из CSV
processed_data = []

with open(csv_file, 'r', encoding='utf-8-sig') as file:
	reader = csv.DictReader(file, delimiter=',')

	for row in reader:
		name = row['name']
		area_name = row['area_name']

		# Используем pd.to_datetime для нормализации формата даты
		published_at_raw = row['published_at']
		try:
			# Преобразуем в datetime и обратно в строку с нужным форматом
			dt = pd.to_datetime(published_at_raw)
			# Форматируем обратно в строку с : в часовом поясе
			published_at = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
			# Добавляем двоеточие в часовой пояс, если его нет
			if published_at[-5] != ':':
				published_at = f"{published_at[:-2]}:{published_at[-2:]}"
		except:
			published_at = published_at_raw

		# Обработка зарплаты
		salary_from = row['salary_from'] if row['salary_from'] else None
		salary_to = row['salary_to'] if row['salary_to'] else None
		currency = row['salary_currency']

		# Если оба поля зарплаты пустые
		if salary_from is None and salary_to is None:
			salary = None
		else:
			# Извлекаем год-месяц для курса валют
			year_month = published_at[:7]  # "YYYY-MM"

			# Получаем курс
			if currency == 'RUR':
				rate = 1.0
			elif year_month in currency_rates and currency in currency_rates[year_month]:
				rate = currency_rates[year_month][currency]
			else:
				rate = None

			# Рассчитываем зарплату
			if rate is not None:
				try:
					if salary_from is not None and salary_to is not None:
						salary_val = (float(salary_from) + float(salary_to)) / 2
					elif salary_from is not None:
						salary_val = float(salary_from)
					elif salary_to is not None:
						salary_val = float(salary_to)
					else:
						salary_val = None

					if salary_val is not None:
						salary = int(salary_val * rate)
					else:
						salary = None
				except:
					salary = None
			else:
				salary = None

		processed_data.append((name, salary, area_name, published_at))

		# Пакетная вставка
		if len(processed_data) >= 1000:
			cursor.executemany(f"""
                INSERT INTO {table_name} (name, salary, area_name, published_at)
                VALUES (?, ?, ?, ?)
            """, processed_data)
			processed_data = []

# Вставляем оставшиеся данные
if processed_data:
	cursor.executemany(f"""
        INSERT INTO {table_name} (name, salary, area_name, published_at)
        VALUES (?, ?, ?, ?)
    """, processed_data)

conn.commit()

# Выводим таблицу
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

conn.close()
# При решении возникло много вопросов "что?" и "как?" ответ на который самому найти не удалось, для решения активно использовался GPT