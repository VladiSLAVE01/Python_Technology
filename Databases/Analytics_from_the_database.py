import pandas as pd
import sqlite3

database_name = input()
table_name = input()
vac_name = input()
conn = sqlite3.connect(database_name)
df_years_salary = pd.read_sql(con=conn, sql=f""" Select 
substr(published_at, 1, 4) AS "Год", round(avg(salary),2) as "Средняя з/п"
from {table_name} Group by substr(published_at, 1, 4)""")

df_years_count = pd.read_sql(con=conn, sql=f"""
SELECT 
    SUBSTR(published_at, 1, 4) AS "Год",
    COUNT(*) AS "Количество вакансий"
FROM {table_name}
WHERE salary IS NOT NULL
GROUP BY SUBSTR(published_at,1,4);
""")

df_years_salary_vac = pd.read_sql(con=conn, sql=f""" Select 
substr(published_at, 1, 4) as "Год", round(avg(salary),2) as "Средняя з/п - {vac_name}"
from {table_name} Where name like '%{vac_name}%' Group by substr(published_at, 1, 4) """)

df_years_count_vac = pd.read_sql(con=conn,
                                 sql=f""" Select substr(published_at, 1, 4) as "Год", Count(name) as "Количество вакансий - {vac_name}"
from {table_name} Where name like '%{vac_name}%' AND salary IS NOT NULL Group by substr(published_at, 1, 4)""")

df_area_salary = pd.read_sql(con=conn, sql=f"""
SELECT area_name AS Город, ROUND(AVG(salary), 2) AS "Уровень зарплат по городам"
FROM {table_name}
GROUP BY area_name
HAVING COUNT(1) >= (SELECT COUNT(1) FROM {table_name}) / 100
ORDER BY 2 DESC, 1 ASC
LIMIT 10
""")

df_area_count = pd.read_sql(con=conn, sql=f"""
SELECT 
    area_name AS 'Город',
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name}) AS 'Доля вакансий'
FROM {table_name}
WHERE area_name IS NOT NULL
    AND area_name != ''
GROUP BY area_name
ORDER BY COUNT(*) DESC
LIMIT 10
"""
                            )