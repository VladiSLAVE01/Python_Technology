import csv
import re


def clean_text_value(value):
	raw_text = str(value) if value is not None else ""
	text_without_html = re.sub(r'<[^>]+>', '', raw_text)

	if '\n' in text_without_html:
		parts = text_without_html.split('\n')
		cleaned_parts = [part.strip() for part in parts if part.strip()]
		final_parts = [" ".join(p.split()) for p in cleaned_parts]
		cleaned_value = "; ".join(final_parts)
	else:
		cleaned_value = " ".join(text_without_html.split()).strip()

	if not cleaned_value:
		cleaned_value = "Нет данных"

	return cleaned_value


def process_row(headers, row):
	if len(row) != len(headers):
		return None

	row_dict = {}
	for j, value in enumerate(row):
		cleaned_value = clean_text_value(value)

		if headers[j] == "key_skills":
			cleaned_value = " ".join(cleaned_value.split())

		row_dict[headers[j]] = cleaned_value

	return row_dict


def count_populated_fields(row_dict):
	populated_fields_count = 0
	for val in row_dict.values():
		if val != "Нет данных":
			populated_fields_count += 1
	return populated_fields_count


def read_and_filter_csv(file_name):
	result = []

	with open(file_name, 'r', encoding='utf-8-sig') as csvfile:
		reader = csv.reader(csvfile)
		headers = next(reader)

		for row in reader:
			row_dict = process_row(headers, row)

			if row_dict is not None:
				populated_fields_count = count_populated_fields(row_dict)

				if populated_fields_count >= len(headers) / 2:
					result.append(row_dict)

	return result


def print_results(result):
	if result:
		for i, entry in enumerate(result):
			for key, value in entry.items():
				print(f"{key}: {value}")
			if i < len(result) - 1:
				print()


def main():
	file_name = input()
	result = read_and_filter_csv(file_name)
	print_results(result)


if __name__ == "__main__":
	main()