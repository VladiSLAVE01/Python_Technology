import csv
from var_dump import var_dump

class Salary(object):
    def __init__(self, header):
        self.salary_from = header.get('salary_from')
        self.salary_to = header.get('salary_to')
        self.salary_gross = header.get('salary_gross')
        self.salary_currency = header.get('salary_currency')

class Vacancy(object):
    def __init__(self, header):

        self.name = header.get('name')
        self.description = header.get('description')
        self.key_skills = header.get('key_skills')
        self.experience_id = header.get('experience_id')
        self.premium = header.get('premium')
        self.employer_name = header.get('employer_name')
        self.salary = Salary(header)
        self.area_name = header.get('area_name')
        self.published_at = header.get('published_at')

def main():
    filename = input()
    vacancies = []

    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Заголовки

        for row in reader:
            vacancy_data = dict(zip(header, row)) # Соединяю ключи(названия) и значения
            vacancies.append(Vacancy(vacancy_data))

    var_dump(vacancies)

if __name__ == "__main__":
    main()