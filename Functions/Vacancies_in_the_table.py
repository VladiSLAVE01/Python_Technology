import csv
from prettytable import PrettyTable
from prettytable import ALL

experience_mapping = {
    "notExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

currency_mapping = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинские лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

output_key_order = [
    "Название",
    "Описание",
    "Навыки",
    "Опыт работы",
    "Премиум-вакансия",
    "Компания",
    "Оклад",
    "Название региона",
    "Дата публикации вакансии"
]

def format_number_with_spaces(num_str):
    num = int(float(num_str))
    return f"{num:,}".replace(",", " ")

def formatter(row):
    formatted_data = {}
    formatted_data["Название"] = row.get("name", "")
    formatted_data["Описание"] = row.get("description", "").rstrip()

    key_skills_raw = row.get("key_skills", "")
    if key_skills_raw:
        skills = key_skills_raw.splitlines()
        formatted_data["Навыки"] = ", ".join(skills)
    else:
        formatted_data["Навыки"] = ""

    formatted_data["Опыт работы"] = experience_mapping.get(row.get("experience_id", ""), "Нет опыта")

    formatted_data["Премиум-вакансия"] = "Да" if row.get("premium", "") == "True" else "Нет"
    formatted_data["Компания"] = row.get("employer_name", "")

    salary_from = row.get("salary_from", "")
    salary_to = row.get("salary_to", "")
    salary_currency_abbr = row.get("salary_currency", "")
    salary_gross_flag = row.get("salary_gross", "")

    formatted_salary_from = format_number_with_spaces(salary_from) if salary_from else ""
    formatted_salary_to = format_number_with_spaces(salary_to) if salary_to else ""

    mapped_currency = currency_mapping.get(salary_currency_abbr, salary_currency_abbr)

    gross_text = " (С вычетом налогов)"
    gross_text = " (Без вычета налогов)" if salary_gross_flag == "True" else " (С вычетом налогов)"
    if salary_from and salary_to:
        salary_string_val = f"{formatted_salary_from} - {formatted_salary_to}"
    elif salary_from:
        salary_string_val = formatted_salary_from
    else:
        salary_string_val = ""

    formatted_data["Оклад"] = f"{salary_string_val} ({mapped_currency}){gross_text}" if salary_string_val else ""

    formatted_data["Название региона"] = row.get("area_name", "")
    formatted_data["Дата публикации вакансии"] = row.get("published_at", "")

    return formatted_data

def truncate_text(text, max_length=100):
    if text and len(text) > max_length:
        return text[:max_length] + "..."
    return text if text else ""

def print_vacancies(filename):
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vacancies = list(reader)

    translated_titles = ["№"] + output_key_order
    table = PrettyTable(translated_titles, max_width=20)

    # Включаем выравнивание по левому краю для всех столбцов
    table.align = "l"

    # Включаем отображение всех границ
    table.hrules = ALL
    table.vrules = ALL

    if not vacancies:
        print("Нет данных")
        return

    for i, row in enumerate(vacancies, 1):
        formatted_row = formatter(row)
        row_values = [i] # Добавляем номер строки

        for key in output_key_order:
            value = formatted_row.get(key, "")

            if isinstance(value, str):
                value = truncate_text(value)

            row_values.append(value)

        table.add_row(row_values)

    print(table)


if __name__ == "__main__":
    filename = input()
    print_vacancies(filename)
