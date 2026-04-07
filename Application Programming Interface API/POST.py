import requests
vacanci = input().strip()
salary = input().strip()
city = input().strip()

BASE_URL = 'http://127.0.0.1:8000/vacancies'

new_product = {
    "name": vacanci,
    "salary": salary,
    "area_name": city
}

response = requests.post(BASE_URL, json=new_product)