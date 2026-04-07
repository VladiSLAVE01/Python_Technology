import csv

FIELD_MAPPING = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата и время публикации вакансии'
}


def csv_reader(file_name):
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        data = list(reader)
    return fieldnames, data


def print_vacancies(fieldnames, vacancies):
    for i, vacancy in enumerate(vacancies):
        for field in fieldnames:
            translated_field = FIELD_MAPPING.get(field, field)
            value = vacancy[field]

            if translated_field == 'Навыки':
                if isinstance(value, str):
                    skills = value.splitlines()
                    value = ", ".join(skills)

            elif str(value).lower() == "true":
                value = "Да"
            elif str(value).lower() == "false":
                value = "Нет"
            if translated_field == 'Описание':
                value = value.rstrip()

            print(f"{translated_field}: {value}")

        if i < len(vacancies) - 1:
            print()


def main():
    file_name = input()
    fieldnames, vacancies = csv_reader(file_name)
    if fieldnames and vacancies:
        print_vacancies(fieldnames, vacancies)


if __name__ == "__main__":
    main()
