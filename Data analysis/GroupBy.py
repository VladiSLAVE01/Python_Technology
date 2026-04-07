import pandas as pd
import numpy as np


def load_and_filter_data(file_path):
	vacancies = pd.read_csv(file_path)
	vacancies = (vacancies[vacancies.salary_currency == 'RUR'])[
		['area_name', 'salary_from', 'salary_to']
	].fillna(-1)
	return vacancies


def process_salary_columns(df):
	df['salary_from'] = np.where(
		df['salary_from'] == -1, df['salary_to'], df['salary_from']
	)
	df['salary_to'] = np.where(
		df['salary_to'] == -1, df['salary_from'], df['salary_to']
	)

	df['salary'] = (df['salary_from'] + df['salary_to']) / 2
	df = df.drop(columns=['salary_from', 'salary_to'])

	return df


def calculate_area_statistics(df):
	# Считаем количество вакансий по регионам
	vacancies_counts = df.area_name.value_counts().to_dict()

	# Суммируем зарплаты по регионам
	areas_sum = {}
	for vacancy in df.to_dict('index').values():
		area_name = vacancy['area_name']
		salary = vacancy['salary']
		areas_sum[area_name] = areas_sum.get(area_name, 0) + salary

	# Вычисляем среднюю зарплату по регионам
	areas_avg = {}
	for area, total_salary in areas_sum.items():
		count = vacancies_counts[area]
		avg_salary = int(round(total_salary / count))
		areas_avg[area] = avg_salary

	return areas_avg


def sort_areas(areas_dict):
	sorted_areas = dict(
		sorted(areas_dict.items(), key=lambda x: (-x[1], x[0]))
	)
	return sorted_areas


def main():
	# Загрузка и фильтрация данных
	vacancies = load_and_filter_data('vacancies_small.csv')

	# Обработка зарплатных данных
	vacancies = process_salary_columns(vacancies)

	# Вычисление статистики по регионам
	areas_stats = calculate_area_statistics(vacancies)

	# Сортировка результатов
	sorted_areas = sort_areas(areas_stats)

	# Вывод результатов
	print(sorted_areas)


if __name__ == "__main__":
	main()