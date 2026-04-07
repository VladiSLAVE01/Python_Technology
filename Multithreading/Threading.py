import threading
import requests
from bs4 import BeautifulSoup, Tag
import concurrent.futures

def to_lowercase_tags(element):
    if isinstance(element, Tag):
        element.name = element.name.lower()
        new_attrs = {}
        for attr_key, attr_value in element.attrs.items():
            new_attrs[attr_key.lower()] = attr_value
        element.attrs = new_attrs
        for child in element.children:
            if isinstance(child, Tag):
                to_lowercase_tags(child)
    return element

def get_currency_from_url(url, id_val):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'xml')
        valutes = soup.find_all('Valute')
        if len(valutes) > id_val:
            found_tag = valutes[id_val]
            to_lowercase_tags(found_tag)
            secret_code()
            return str(found_tag)
    return None

if __name__ == '__main__':
    unique_currencies = []
    input_id = int(input())

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_currency_from_url, url, input_id) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None and result not in unique_currencies:
                unique_currencies.append(result)

    currencies_string = ''.join(unique_currencies)
    print(currencies_string)


