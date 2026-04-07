import pandas as pd
import re


def remove_html_tags(text):
    return re.sub(r'<[^>]+>', '', str(text))


def clean_html_in_dataframe(df):
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].apply(remove_html_tags)
    return df


def filter_dataframe(df, filter_column, substring):
    filtered = df[df[filter_column].str.contains(substring, case=False, na=False)].copy()
    filtered['original_index'] = filtered.index
    return filtered


def sort_and_extract(df, sort_column, sort_type, target_column='name'):
    ascending = sort_type == 'asc'
    sorted_df = df.sort_values(by=[sort_column, 'original_index'], ascending=[ascending, True])
    return sorted_df[target_column].tolist()


def main():
    filter_column = input()
    substring = input()
    sort_column = input()
    sort_type = input()

    # Чтение и очистка данных
    vacancies = pd.read_csv('vacancies_small.csv')
    cleaned_vacancies = clean_html_in_dataframe(vacancies)

    # Фильтрация
    filtered_vacancies = filter_dataframe(cleaned_vacancies, filter_column, substring)

    # Сортировка и получение результата
    result = sort_and_extract(filtered_vacancies, sort_column, sort_type)

    # Вывод результата
    print(result)


if __name__ == "__main__":
    main()