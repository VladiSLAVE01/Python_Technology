import re
import json

str1 = input()

str2 = input()

def check_company_info(company_info_str):
    str = company_info_str
    while '(' in str or ')' in str:
        str = re.sub(r'\([^()]*\)','', str)
    return str

def check_description(description_str):
    values = description_str.split('. ')
    for i in range(len(values)):
        values[i] = values[i].capitalize()
    return '. '.join(values)

functions_rules = {
    'description': check_description,
    'salary': lambda salary_str: str(format(round(float(salary_str),2), '.2f')),
    'key_phrase': lambda key_phrase_str: f'{key_phrase_str.upper()}!',
    'addition': lambda addition_str: f'..{addition_str.lower()}..',
    'company_info': check_company_info,
    'key_skills': lambda key_skills_str: key_skills_str.replace('&nbsp',' '),
}

splitted_values = str1.split(';')
result = {}
for value in splitted_values:
    if not value:
        continue
    arr = value.split(':')
    key_dict = arr[0].strip()
    if key_dict in str2:
        value_dict = functions_rules[key_dict](arr[1].strip())
        result[key_dict] = value_dict
print(json.dumps(result))