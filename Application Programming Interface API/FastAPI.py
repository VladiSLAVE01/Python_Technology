import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from contextlib import contextmanager


class VacancyCreate(BaseModel):
	name: str
	salary: str
	area_name: str


app = FastAPI()


@contextmanager
def db_session():
	connection = sqlite3.connect('vacancies.db')
	connection.row_factory = sqlite3.Row
	yield connection
	connection.close()


@app.get("/vacancies/{vacancy_id}")
def get_vacancy_endpoint(vacancy_id: int):
	with db_session() as session:
		query_runner = session.cursor()
		query_runner.execute(
			"SELECT id, name, salary, area_name, published_at FROM vacancies WHERE id = ?",
			(vacancy_id,)
		)
		result_row = query_runner.fetchone()

		if not result_row:
			return {"error": "vacancy not found"}

		return {
			"id": result_row[0],
			"name": result_row[1],
			"salary": result_row[2],
			"area_name": result_row[3],
			"published_at": result_row[4]
		}


@app.post("/vacancies")
def create_vacancy_endpoint(vacancy_request: VacancyCreate):
	with db_session() as session:
		cursor_obj = session.cursor()

		# Получаем максимальный ID
		cursor_obj.execute("SELECT MAX(id) FROM vacancies")
		max_id_data = cursor_obj.fetchone()
		last_id_value = max_id_data[0] if max_id_data[0] is not None else 0

		# Генерируем новый ID и время
		new_identifier = last_id_value + 1
		current_timestamp = datetime.now().isoformat()

		# Вставляем новую запись
		cursor_obj.execute(
			"""
			INSERT INTO vacancies (id, name, salary, area_name, published_at)
			VALUES (?, ?, ?, ?, ?)
			""",
			(new_identifier, vacancy_request.name, vacancy_request.salary,
			 vacancy_request.area_name, current_timestamp)
		)

		session.commit()

	return {"message": "vacancy posted successfully"}


@app.delete("/vacancies/{vacancy_id}")
def delete_vacancy_endpoint(vacancy_id: int):
	with db_session() as session:
		cursor_obj = session.cursor()

		# Проверяем существование
		cursor_obj.execute("SELECT 1 FROM vacancies WHERE id = ?", (vacancy_id,))
		exists_check = cursor_obj.fetchone()

		if not exists_check:
			return {"error": "vacancy not found"}

		# Удаляем запись
		cursor_obj.execute("DELETE FROM vacancies WHERE id = ?", (vacancy_id,))
		session.commit()

	return {"message": "vacancy deleted successfully"}


def initialize_database():
	connection = sqlite3.connect('vacancies.db')
	cursor = connection.cursor()
	cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary TEXT,
            area_name TEXT,
            published_at TEXT
        )
    """)
	connection.commit()
	connection.close()


initialize_database()