from bs4 import BeautifulSoup
import json
import re

exchange = {
	'₽': 1.0,
	'$': 100.0,
	'€': 105.0,
	'₸': 0.210,
	'Br': 30.0,
}


def extract_title(soup):
	title_element = soup.select_one('.vacancy-title')
	if not title_element:
		return ""

	title_text = title_element.get_text(' ', strip=False).strip().split('\n')[0]
	cleaned_title = re.sub(r'до\s*\d+[\d\s]*[₽|$|€|₸|Br].*$', '', title_text)
	cleaned_title = re.sub(r'от\s*\d+[\d\s]*[₽|$|€|₸|Br].*$', '', cleaned_title)
	cleaned_title = re.sub(r'\d+[\d\s]*[₽|$|€|₸|Br].*$', '', cleaned_title)
	cleaned_title = re.sub(r'\d', '', cleaned_title)
	cleaned_title = re.sub(r' от ', '', cleaned_title)

	return cleaned_title.strip()


def extract_salary(soup):
	title_element = soup.select_one('.vacancy-title')
	if not title_element:
		return ""

	title_text = title_element.get_text(' ', strip=False).strip()
	salary_item = title_text.replace('\xa0', '')
	salary_matches = re.findall(r'\d+', salary_item)

	salary_count = 0
	salary_value1 = 0
	salary_value2 = 0
	currency_value = "₽"

	for salary_match in salary_matches:
		if salary_count == 0:
			salary_count = 1
			salary_value1 = salary_match
			continue
		if salary_count == 1:
			salary_count = 2
			salary_value2 = salary_match

	for currency in ['₽', '$', '€', '₸', 'Br']:
		if currency in salary_item:
			currency_value = currency
			break

	if salary_count == 1:
		return str(int(salary_value1) * exchange[currency_value])
	elif salary_count == 2:
		return f"{str(int(salary_value1) * exchange[currency_value])}->{str(int(salary_value2) * exchange[currency_value])}"
	else:
		return ""


def extract_experience(soup):
	experience_element = soup.select_one(".vacancy-description-list-item")
	if not experience_element:
		return None

	experience_text = experience_element.get_text().strip().split('\n')
	numbers_count = 0
	first_number = 0
	second_number = 0

	for item in experience_text:
		item_numbers = re.findall(r'\d', item)
		for number in item_numbers:
			if numbers_count == 0:
				numbers_count = 1
				first_number = number
				continue
			if numbers_count == 1:
				numbers_count = 2
				second_number = number

	if numbers_count == 0:
		return None
	elif numbers_count == 1:
		return first_number
	else:
		return f"{first_number}-{second_number}"


def extract_company(soup):
	company_element = soup.select_one(".vacancy-company-name")
	if company_element:
		return company_element.get_text().strip().split("\n")[0]
	return ""


def extract_description(soup):
	description_element = soup.find(attrs={"data-qa": "vacancy-description"})
	if description_element:
		return description_element.get_text('', strip=False).replace("\n", "")
	return ""


def extract_skills(soup):
	skills_element = soup.select('.vacancy-section')
	if len(skills_element) > 2:
		skills_text = skills_element[2].get_text("; ", strip=False)
		return '; '.join(skills_text.split("; ")[1:])
	return ""


def extract_creation_time(soup):
	creation_time_element = soup.select_one(".vacancy-creation-time-redesigned")
	if creation_time_element:
		creation_date_text = creation_time_element.get_text().replace('\xa0', ' ').strip()
		date_matches = re.findall(r'\d.*\d', creation_date_text)
		if date_matches:
			return date_matches[0]
	return ""


def parse_vacancy(html_content):
	soup = BeautifulSoup(open(html_content), 'html.parser')

	vacancy_data = {
		'vacancy': extract_title(soup),
		'salary': extract_salary(soup),
		'experience': extract_experience(soup),
		'company': extract_company(soup),
		'description': extract_description(soup),
		'skills': extract_skills(soup),
		'created_at': extract_creation_time(soup),
	}

	return vacancy_data


def main():
	html = input()
	result = parse_vacancy(html)
	print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
	main()