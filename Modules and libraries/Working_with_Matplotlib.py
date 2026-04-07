import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict
from datetime import datetime
import textwrap


def read_vacancies_data(file_path, profession_name):
	salary_by_year = defaultdict(list)
	count_by_year = defaultdict(int)
	prof_salary_by_year = defaultdict(list)
	prof_count_by_year = defaultdict(int)
	salary_by_city = defaultdict(list)
	count_by_city = defaultdict(int)
	total_vacancies = 0

	with open(file_path, 'r', encoding='utf-8') as file:
		reader = csv.reader(file)
		for row in reader:
			if len(row) < 6:
				continue

			vacancy_name, salary_from, salary_to, currency, city, date_str = row

			try:
				salary_from = float(salary_from)
				salary_to = float(salary_to)
				date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
				year = date.year
			except (ValueError, TypeError):
				continue

			if year < 2007 or year > 2022 or currency != 'RUR':
				continue

			avg_salary = (salary_from + salary_to) / 2
			salary_by_year[year].append(avg_salary)
			salary_by_city[city].append(avg_salary)
			count_by_year[year] += 1
			count_by_city[city] += 1
			total_vacancies += 1

			if profession_name.lower() in vacancy_name.lower():
				prof_salary_by_year[year].append(avg_salary)
				prof_count_by_year[year] += 1

	return salary_by_year, count_by_year, prof_salary_by_year, prof_count_by_year, \
		salary_by_city, count_by_city, total_vacancies


def prepare_yearly_statistics(years_range, salary_by_year, count_by_year,
                              prof_salary_by_year, prof_count_by_year):
	"""Подготовка статистики по годам."""
	years = list(years_range)

	counts = [count_by_year.get(year, 0) for year in years]
	salaries = [
		round(sum(salary_by_year[year]) / len(salary_by_year[year])) if salary_by_year[year] else 0
		for year in years
	]

	prof_counts = [prof_count_by_year.get(year, 0) for year in years]
	prof_salaries = [
		round(sum(prof_salary_by_year[year]) / len(prof_salary_by_year[year])) if prof_salary_by_year[year] else 0
		for year in years
	]

	return years, counts, salaries, prof_counts, prof_salaries


def prepare_city_statistics(salary_by_city, count_by_city, total_vacancies, min_share=1.0, top_n=10):
	average_salaries_city = {
		city: sum(salaries) / len(salaries)
		for city, salaries in salary_by_city.items()
		if salaries
	}

	vacancy_shares = {
		city: round((count / total_vacancies) * 100, 2)
		for city, count in count_by_city.items()
		if total_vacancies > 0
	}

	filtered_cities = {
		city for city, share in vacancy_shares.items()
		if share > min_share
	}

	city_salaries = sorted(
		[
			(city, round(avg_salary))
			for city, avg_salary in average_salaries_city.items()
			if city in filtered_cities
		],
		key=lambda x: (-x[1], x[0])
	)[:top_n]

	city_shares = sorted(
		[
			(city, share)
			for city, share in vacancy_shares.items()
			if city in filtered_cities
		],
		key=lambda x: (-x[1], x[0])
	)[:top_n]

	return city_salaries, city_shares


def load_data_once(profession_name, file_path='vacancies.csv'):
	salary_by_year, count_by_year, prof_salary_by_year, prof_count_by_year, \
		salary_by_city, count_by_city, total_vacancies = read_vacancies_data(file_path, profession_name)

	years, counts, salaries, prof_counts, prof_salaries = prepare_yearly_statistics(
		range(2007, 2023), salary_by_year, count_by_year, prof_salary_by_year, prof_count_by_year
	)

	city_salaries, city_shares = prepare_city_statistics(
		salary_by_city, count_by_city, total_vacancies
	)

	return years, counts, salaries, prof_counts, prof_salaries, city_salaries, city_shares


def create_salary_by_year_plot(ax, years, salaries, prof_salaries, profession_name):
	x = np.arange(len(years))
	width = 0.35

	ax.bar(x - width / 2, salaries, width, label='средняя з/п')
	ax.bar(x + width / 2, prof_salaries, width, label=f'з/п {profession_name}')
	ax.set_title('Уровень зарплат по годам', fontsize=8)
	ax.legend(fontsize=8)
	ax.grid(True, alpha=0.3, axis='y')
	ax.tick_params(axis='x', rotation=90, labelsize=8)
	ax.tick_params(axis='y', labelsize=8)
	ax.set_xticks(x)
	ax.set_xticklabels(years)

	return ax


def create_vacancies_by_year_plot(ax, years, counts, prof_counts, profession_name):
	x = np.arange(len(years))
	width = 0.35

	ax.bar(x - width / 2, counts, width, label='Количество вакансий')
	ax.bar(x + width / 2, prof_counts, width, label=f'Количество вакансий\n{profession_name}')
	ax.set_title('Количество вакансий по годам', fontsize=8)
	ax.legend(fontsize=8)
	ax.grid(True, alpha=0.3, axis='y')
	ax.tick_params(axis='x', rotation=90, labelsize=8)
	ax.set_xticks(x)
	ax.set_xticklabels(years)

	return ax


def create_salary_by_city_plot(ax, city_salaries):
	"""Создание графика уровня зарплат по городам."""
	cities = [city for city, salary in city_salaries]
	salaries_values = [salary for city, salary in city_salaries]

	processed_cities = []
	for city in cities:
		if ' ' in city or '-' in city:
			processed_cities.append(textwrap.fill(city, width=15))
		else:
			processed_cities.append(city)

	ax.barh(processed_cities, salaries_values)
	ax.set_title('Уровень зарплат по городам', fontsize=8)
	ax.grid(True, alpha=0.3, axis='x')
	ax.tick_params(axis='y', labelsize=6)
	ax.tick_params(axis='x', labelsize=8)

	for label in ax.get_yticklabels():
		label.set_horizontalalignment('right')
		label.set_verticalalignment('center')

	return ax


def create_vacancy_share_by_city_plot(ax, city_shares):
	cities_pie = [city for city, share in city_shares]
	shares = [share for city, share in city_shares]

	if len(shares) > 10:
		other_share = 100 - sum(shares[:10])
		cities_pie = cities_pie[:10] + ['Другие']
		shares = shares[:10] + [other_share]
	else:
		cities_pie = cities_pie + ['Другие']
		shares = shares + [0]

	colors = plt.cm.Set3(np.linspace(0, 1, len(shares)))
	wedges, texts, autotexts = ax.pie(
		shares, labels=cities_pie, autopct='%1.1f%%',
		colors=colors, startangle=90
	)
	ax.set_title('Доля вакансий по городам', fontsize=8)

	for text in texts:
		text.set_fontsize(6)
	for autotext in autotexts:
		autotext.set_fontsize(6)
		autotext.set_color('black')
		autotext.set_fontweight('bold')

	return ax


def all_create_plot(subplots, profession_name):
	years, counts, salaries, prof_counts, prof_salaries, city_salaries, city_shares = load_data_once(profession_name)

	plt.rcParams['font.size'] = 8

	# 1. Уровень зарплат по годам
	create_salary_by_year_plot(subplots[0, 0], years, salaries, prof_salaries, profession_name)

	# 2. Количество вакансий по годам
	create_vacancies_by_year_plot(subplots[0, 1], years, counts, prof_counts, profession_name)

	# 3. Уровень зарплат по городам
	create_salary_by_city_plot(subplots[1, 0], city_salaries)

	# 4. Доля вакансий по городам
	create_vacancy_share_by_city_plot(subplots[1, 1], city_shares)

	plt.tight_layout()
	return subplots


def create_plot(profession_name=None):
	"""Основная функция для создания графиков."""
	if profession_name is None:
		profession_name = input().lower()

	fig, sub = plt.subplots(2, 2, figsize=(15, 10))
	all_create_plot(sub, profession_name)
	plt.show()
	return fig


if __name__ == "__main__":
	create_plot()