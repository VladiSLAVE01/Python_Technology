from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd


def get_vacancy_by_id(id):
    return data.iloc[id].to_dict()


def get_vacancies_by_city(city):
    job_listings = data[data['Город'] == city].to_dict(orient='index')
    job_listings = dict(map(lambda item: (str(item[0]), item[1]), job_listings.items()))
    return job_listings


def get_vacancies_by_min_salary(salary):
    job_openings = data[data['Зарплата от'] >= salary].to_dict(orient='index')
    job_openings = dict(map(lambda item: (str(item[0]), item[1]), job_openings.items()))
    return job_openings


def exit_server():
    server.quit = 1
    return 1


def start_server():
    global data
    data = pd.read_csv('vacancies.csv', names=['name', 'salary_from', 'salary_to', 'currency', 'city', 'published_at'])
    data = data.rename(columns={'name': 'Название вакансии', 'salary_from': 'Зарплата от', 'salary_to': 'Зарплата до', 'city': 'Город'})
    data = data.drop(columns=['currency', 'published_at'])
    global server
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_function(get_vacancy_by_id, 'get_vacancy_by_id')
    server.register_function(get_vacancies_by_city, 'get_vacancies_by_city')
    server.register_function(get_vacancies_by_min_salary, 'get_vacancies_by_min_salary')
    server.register_function(exit_server, 'exit')
    server.serve_forever()


if __name__ == "__main__":
    start_server()