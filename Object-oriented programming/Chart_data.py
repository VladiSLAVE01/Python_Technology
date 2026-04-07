import csv
import sys
from datetime import datetime

# Provided currency_to_rub dictionary - Make it global as per initial skeleton
currency_to_rub = {
	"Манаты": 35.68,
	"Белорусские рубли": 23.91,
	"Евро": 59.90,
	"Грузинский лари": 21.74,
	"Киргизский сом": 0.76,
	"Тенге": 0.13,
	"Рубли": 1,
	"Гривны": 1.64,
	"Доллары": 60.66,
	"Узбекский сум": 0.0055,
}


class Salary:
	"""Устанавливает все основные поля зарплаты и предоставляет метод для расчета средней зарплаты в рублях."""

	def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
		try:
			self.salary_from = float(salary_from) if salary_from else 0.0
			self.salary_to = float(salary_to) if salary_to else 0.0
		except ValueError:
			self.salary_from = 0.0
			self.salary_to = 0.0
		self.salary_gross = salary_gross
		self.salary_currency = salary_currency

	def get_average_in_rubles(self):

		if self.salary_from == 0.0 and self.salary_to == 0.0:
			return None  # Исключаем из расчетов, если оба поля зарплаты пустые

		avg_salary = (self.salary_from + self.salary_to) / 2

		if self.salary_currency in currency_to_rub:
			return avg_salary * currency_to_rub[self.salary_currency]
		else:
			return None  # Неизвестная валюта, не можем конвертировать


class Vacancy:
	def __init__(self, data_row, headers):
		vacancy_data = dict(zip(headers, data_row))

		self.name = vacancy_data.get("name", "")
		self.salary = Salary(
			vacancy_data.get("salary_from", ""),
			vacancy_data.get("salary_to", ""),
			vacancy_data.get("salary_gross", ""),
			vacancy_data.get("salary_currency", "")
		)
		self.area_name = vacancy_data.get("area_name", "")

		published_at_str = vacancy_data.get("published_at", "")
		self.year = None
		if published_at_str:
			dt_object = datetime.fromisoformat(published_at_str.split('+')[0])
			self.year = dt_object.year
			pass


class DataSet:

	def __init__(self, filename):
		self.filename = filename
		self.headers = []
		self.vacancies = []
		self._load_data()

	def _load_data(self):
		with open(self.filename, mode='r', encoding='utf-8-sig') as csvfile:
			reader = csv.reader(csvfile)

			for row in reader:
				if not row or len(row) != len(self.headers) or any(not field.strip() for field in row):
					continue

				self.vacancies.append(Vacancy(row, self.headers))


class Statistics:
	def __init__(self, dataset):
		self.vacancies = dataset.vacancies
		self.total_vacancies_count = len(self.vacancies)

	def _get_salary_by_year(self, profession_name=None):
		salaries_by_year = {}
		for vacancy in self.vacancies:
			if vacancy.year is None:
				continue

			if profession_name and profession_name.lower() not in vacancy.name.lower():
				continue

			avg_rub_salary = vacancy.salary.get_average_in_rubles()
			if avg_rub_salary is not None:
				if vacancy.year not in salaries_by_year:
					salaries_by_year[vacancy.year] = []
				salaries_by_year[vacancy.year].append(avg_rub_salary)

		result = {year: int(sum(s) / len(s)) for year, s in salaries_by_year.items() if s}
		return dict(sorted(result.items()))

	def _get_vacancy_count_by_year(self, profession_name=None):
		count_by_year = {}
		for vacancy in self.vacancies:
			if vacancy.year is None:
				continue

			if profession_name and profession_name.lower() not in vacancy.name.lower():
				continue

			count_by_year[vacancy.year] = count_by_year.get(vacancy.year, 0) + 1

		return dict(sorted(count_by_year.items()))

	def _get_vacancy_count_by_city(self):
		count_by_city = {}
		for vacancy in self.vacancies:
			if not vacancy.area_name:
				continue
			count_by_city[vacancy.area_name] = count_by_city.get(vacancy.area_name, 0) + 1
		return count_by_city

	def _get_salary_by_city(self):
		salaries_by_city = {}
		city_counts = self._get_vacancy_count_by_city()

		if self.total_vacancies_count == 0:
			return {}

		for vacancy in self.vacancies:
			if not vacancy.area_name:
				continue

			# Проверяем правило 1% до добавления в список зарплат
			if city_counts.get(vacancy.area_name, 0) / self.total_vacancies_count < 0.01:
				continue

			avg_rub_salary = vacancy.salary.get_average_in_rubles()
			if avg_rub_salary is not None:
				if vacancy.area_name not in salaries_by_city:
					salaries_by_city[vacancy.area_name] = []
				salaries_by_city[vacancy.area_name].append(avg_rub_salary)

		# Вычисляем средние значения для отфильтрованных городов
		result = {city: int(sum(s) / len(s)) for city, s in salaries_by_city.items() if s}

		# Сортируем по убыванию зарплаты и берем топ-10
		sorted_cities = sorted(result.items(), key=lambda item: item[1], reverse=True)
		return dict(sorted_cities[:10])

	def _get_vacancy_share_by_city(self):
		city_counts = self._get_vacancy_count_by_city()
		if self.total_vacancies_count == 0:
			return {}

		share_by_city = {}
		for city, count in city_counts.items():
			share = count / self.total_vacancies_count
			if share >= 0.01:  # Фильтруем города с долей менее 1%
				share_by_city[city] = round(share, 2)  # Округляем до 2 знаков после запятой

		# Сортируем по убыванию доли, затем по названию города (по возрастанию)
		sorted_cities = sorted(share_by_city.items(), key=lambda item: (-item[1], item[0]))
		return dict(sorted_cities[:10])

	def get_all_statistics(self, profession_name):
		salary_by_year = self._get_salary_by_year()
		count_by_year = self._get_vacancy_count_by_year()
		salary_by_year_prof = self._get_salary_by_year(profession_name)
		count_by_year_prof = self._get_vacancy_count_by_year(profession_name)
		salary_by_city = self._get_salary_by_city()
		share_by_city = self._get_vacancy_share_by_city()

		return salary_by_year, count_by_year, salary_by_year_prof, count_by_year_prof, salary_by_city, share_by_city


def main():
	filename = input()
	profession_name = input()

	dataset = DataSet(filename)
	statistics = Statistics(dataset)

	(salary_by_year, count_by_year,
	 salary_by_year_prof, count_by_year_prof,
	 salary_by_city, share_by_city) = statistics.get_all_statistics(profession_name)

	print(f"Динамика уровня зарплат по годам: {salary_by_year}")
	print(f"Динамика количества вакансий по годам: {count_by_year}")
	print(f"Динамика уровня зарплат по годам для выбранной профессии {profession_name}: {salary_by_year_prof}")
	print(f"Динамика количества вакансий по годам для выбранной профессии {profession_name}: {count_by_year_prof}")
	print(f"Уровень зарплат по городам (в порядке убывания): {salary_by_city}")
	print(f"Доля вакансий по городам (в порядке убывания): {share_by_city}")


if __name__ == '__main__':
	main()