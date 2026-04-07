import math

# ниже склоняет слова)
def pluralize(amount, years):
    amount = int(amount)
    if amount % 10 == 1 and amount % 100 != 11:
        suffix = {
            "год": " год",
            "рубль": " рубль"
        }.get(years, "")
    elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        suffix = {
            "год": " года",
            "рубль": " рубля"
        }.get(years, "")
    else:
        suffix = {
            "год": " лет",
            "рубль": " рублей"
        }.get(years, "")
    return f"{amount}{suffix}"

#ввод данных
title = input("Введите название вакансии: ")
description = input("Введите описание вакансии: ")
city = input("Введите город для вакансии: ")
experience = int(input("Введите требуемый опыт работы (лет): "))
salary_min = int(input("Введите нижнюю границу оклада вакансии: "))
salary_max = int(input("Введите верхнюю границу оклада вакансии: "))
flexible_schedule = input("Нужен свободный график (да / нет): ")
premium_vacancy = input("Является ли данная вакансия премиум-вакансией (да / нет): ")

average_salary = math.floor((salary_min + salary_max) / 2)

# форматирование ввода
print(title)
print(f"Описание: {description}")
print(f"Город: {city}")
print(f"Требуемый опыт работы: {pluralize(experience, 'год')}")
print(f"Средний оклад: {pluralize(average_salary, 'рубль')}")

# обработка логических выражений
def print_boolean_status(variable, name):
    status = "да" if str(variable).lower() == "да" else "нет"
    print(f"{name}: {status}")

print_boolean_status(flexible_schedule, "Свободный график")
print_boolean_status(premium_vacancy, "Премиум-вакансия")