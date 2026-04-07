import csv
import re
import math
from collections import Counter

def declension(n, variants):
    """Возвращает правильную форму слова в зависимости от числа."""
    if n % 10 == 1 and n % 100 != 11:
        return variants[0]
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return variants[1]
    else:
        return variants[2]

def clean_html(text):
    """Удаляет HTML-теги и лишние пробелы."""
    cleaned_text = re.sub(r'<[^>]+>', '', text)
    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text.strip()

file_name = input()

vacancies = []

with open(file_name, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['salary_currency'] == 'RUR':
            vacancies.append(row)

for vacancy in vacancies:
    try:
        salary_from = int(vacancy['salary_from'])
        salary_to = int(vacancy['salary_to'])
        vacancy['average_salary'] = math.floor((salary_from + salary_to) / 2)
        vacancy['employer_name'] = clean_html(vacancy['employer_name'])
        vacancy['name'] = clean_html(vacancy['name'])
        vacancy['area_name'] = clean_html(vacancy['area_name'])
    except ValueError:
        vacancies.remove(vacancy)
        continue

print("Самые высокие зарплаты:")
for i, vacancy in enumerate(top_salaries):
    print(f"{i+1:2}) {vacancy['name']} в компании \"{vacancy['employer_name']}\" - {vacancy['average_salary']} рублей (г. {vacancy['area_name']})")
print()

print("Самые низкие зарплаты:")
for i, vacancy in enumerate(bottom_salaries):
    print(f"{i+1:2}) {vacancy['name']} в компании \"{vacancy['employer_name']}\" - {vacancy['average_salary']} рублей (г. {vacancy['area_name']})")
print()

all_skills = []
for vacancy in vacancies:
    skills = vacancy['key_skills'].split("; ")
    all_skills.extend(skills)

skill_counts = Counter(all_skills)
most_common_skills = skill_counts.most_common(7)

print("Из {} скиллов, самые популярные являются:".format(len(set(all_skills))))
for i, (skill, count) in enumerate(most_common_skills):
    times_word = declension(count, [" раз", " раза", " раз"])
    print(f"{i+1:2}) {skill} - упоминается {count}{times_word}")
print()

city_salaries = {}
for vacancy in vacancies:
    city = vacancy['area_name']
    salary = vacancy['average_salary']
    if city in city_salaries:
        city_salaries[city]['total_salary'] += salary
        city_salaries[city]['count'] += 1
    else:
        city_salaries[city] = {'total_salary': salary, 'count': 1}

total_vacancies = len(vacancies)
one_percent_threshold = math.floor(0.01 * total_vacancies)
eligible_cities = {
    city: data
    for city, data in city_salaries.items()
    if data['count'] >= one_percent_threshold
}

for city, data in eligible_cities.items():
  eligible_cities[city]['average_salary'] = math.floor(data['total_salary'] / data['count'])

sorted_cities = sorted(eligible_cities.items(), key=lambda item: item[1]['average_salary'], reverse=True)[:2]

print("Из {} городов, самые высокие средние ЗП:".format(len(city_salaries)))
for i, (city, data) in enumerate(sorted_cities):
    print(f"{i+1:2}) {city} - средняя зарплата {data['average_salary']} рублей ({data['count']} {declension(data['count'], ['вакансия', 'вакансии', 'вакансий'])})")
