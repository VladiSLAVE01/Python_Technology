import pandas as pd
import sqlite3


def convert_salary_to_rubles(df_rates, vacancy_row):
    if vacancy_row['salary_currency'] == 'RUR':
        return vacancy_row['avg_salary']

    if vacancy_row['year_month'] in df_rates.index and vacancy_row['salary_currency'] in df_rates.columns:
        exchange_rate = df_rates.at[vacancy_row['year_month'], vacancy_row['salary_currency']]
        return vacancy_row['avg_salary'] * exchange_rate

    return None


def calculate_mean_salary(vacancy_row):
    salary_bounds = [vacancy_row['salary_from'], vacancy_row['salary_to']]
    non_nan_salaries = [value for value in salary_bounds if not pd.isna(value)]

    if non_nan_salaries:
        return sum(non_nan_salaries) / len(non_nan_salaries)
    return None


def load_and_process_vacancies(vacancies_csv, rates_csv):
    df_exchange_rates = pd.read_csv(rates_csv, index_col='date')
    df_job_vacancies = pd.read_csv(vacancies_csv)

    # Добавляем уникальный идентификатор
    df_job_vacancies['id'] = df_job_vacancies.index + 1

    # Извлекаем год и месяц из даты публикации
    df_job_vacancies['year_month'] = pd.to_datetime(
        df_job_vacancies['published_at'],
        errors='coerce',
        utc=True
    ).dt.strftime('%Y-%m')

    # Вычисляем среднюю зарплату для каждой вакансии
    df_job_vacancies['avg_salary'] = df_job_vacancies.apply(calculate_mean_salary, axis=1)

    # Конвертируем зарплаты в рубли
    df_job_vacancies['salary_in_rub'] = df_job_vacancies.apply(
        lambda row: convert_salary_to_rubles(df_exchange_rates, row),
        axis=1
    )

    # Выбираем только необходимые столбцы для базы данных
    result_columns = ['id', 'name', 'salary_in_rub', 'area_name', 'published_at']
    return df_job_vacancies[result_columns]


def store_to_sqlite(data_table, database_path):
    with sqlite3.connect(database_path) as db_connection:
        data_table.set_index('id').to_sql(
            'vacancies',
            db_connection,
            if_exists='replace'
        )


def execute_pipeline():
    input_vacancies_file = 'vacancies_dif_currencies.csv'
    input_rates_file = 'valutes.csv'
    output_database = 'student_works/vacancies.db'

    processed_data = load_and_process_vacancies(input_vacancies_file, input_rates_file)

    store_to_sqlite(processed_data, output_database)


if __name__ == "__main__":
    execute_pipeline()