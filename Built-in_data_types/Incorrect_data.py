import math

def pluralize_years(years):
    years = int(years)
    if years % 10 == 1 and years % 100 != 11:
        return f"{years} год"
    elif 2 <= years % 10 <= 4 and (years % 100 < 10 or years % 100 >= 20):
        return f"{years} года"
    else:
        return f"{years} лет"

def pluralize_rubles(amount):
    amount = int(amount)
    if amount % 10 == 1 and amount % 100 != 11:
        return f"{amount} рубль"
    elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        return f"{amount} рубля"
    else:
        return f"{amount} рублей"

def get_valid_input(prompt, data_type):
    while True:
        user_input = input(prompt).strip()
        if data_type == str:
            if not user_input:
                print("Данные некорректны, повторите ввод")
                continue
            return user_input
        elif data_type == int:
            # Проверка без try/except
            if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
                return int(user_input)
            else:
                print("Данные некорректны, повторите ввод")
                continue
        elif data_type == bool:
            user_input = user_input.lower()
            if user_input not in ("да", "нет"):
                print("Данные некорректны, повторите ввод")
                continue
            return user_input == "да"

# ввод данных
title = None
while title is None:
    title = get_valid_input("Введите название вакансии: ", str)

description = None
while description is None:
    description = get_valid_input("Введите описание вакансии: ", str)

city = None
while city is None:
    city = get_valid_input("Введите город для вакансии: ", str)

experience = None
while experience is None:
    experience = get_valid_input("Введите требуемый опыт работы (лет): ", int)

# Бесконечный цикл, пока не будут введены корректные значения salary_min и salary_max
while True:
    salary_min = get_valid_input("Введите нижнюю границу оклада вакансии: ", int)
    salary_max = get_valid_input("Введите верхнюю границу оклада вакансии: ", int)
    if salary_min > salary_max:
        print("Нижняя граница оклада должна быть не больше верхней границы. Повторите ввод.")
        continue
    else:
        break

flexible_schedule = get_valid_input("Нужен свободный график (да / нет): ", bool)
premium_vacancy = get_valid_input("Является ли данная вакансия премиум-вакансией (да / нет): ", bool)

average_salary = math.floor((salary_min + salary_max) / 2)

# Форматирование ввода
print(title)
print(f"Описание: {description}")
print(f"Город: {city}")
print(f"Требуемый опыт работы: {pluralize_years(experience)}")
print(f"Средний оклад: {pluralize_rubles(average_salary)}")

# обработка логических выражений (Теперь можно просто использовать True/False)
print("Свободный график:", "да" if flexible_schedule else "нет")
print("Премиум-вакансия:", "да" if premium_vacancy else "нет")