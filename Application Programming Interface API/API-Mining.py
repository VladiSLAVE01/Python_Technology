import pandas as pd
import requests
from lxml import etree
from datetime import datetime

START_DATE = '2003-01-01'
END_DATE = '2024-11-01'
CURRENCY_CODES = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']


def fetch_exchange_rates(start, end, codes):
	current = datetime.strptime(start, '%Y-%m-%d')
	end_date = datetime.strptime(end, '%Y-%m-%d')
	data_collected = []

	while current <= end_date:
		date_str = current.strftime('%d/%m/%Y')
		response = requests.get(f'http://127.0.0.1:8000/scripts/XML_daily.asp?date_req={date_str}')
		xml_data = etree.fromstring(response.content)
		month_period = current.strftime('%Y-%m')
		row_data = [month_period]

		for code in codes:
			valute_node = xml_data.xpath(f"//Valute[CharCode='{code}']")
			rate_value = (
				float(valute_node[0].find('Value').text.replace(',', '.')) / int(valute_node[0].find('Nominal').text)
				if valute_node else None
			)
			row_data.append(round(rate_value, 8) if rate_value else None)

		data_collected.append(row_data)
		current = (
			current.replace(year=current.year + 1, month=1) if current.month == 12 else current.replace(
				month=current.month + 1)
		)

	return data_collected


def export_to_csv(dataset, columns, filename):
	df = pd.DataFrame(dataset, columns=['date'] + columns)
	df.to_csv(filename, index=False)


if __name__ == "__main__":
	rates_data = fetch_exchange_rates(START_DATE, END_DATE, CURRENCY_CODES)
	export_to_csv(rates_data, CURRENCY_CODES, 'student_works/currency.csv')