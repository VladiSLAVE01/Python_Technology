import requests

city = input().strip()

# Перебираем ID от 1 до 100 (разумный лимит)
for i in range(1, 101):
	response = requests.get(f"http://127.0.0.1:8000/vacancies/{i}")

	if response.status_code == 200:
		vacancy = response.json()
		if vacancy.get("area_name") == city:
			print(vacancy)