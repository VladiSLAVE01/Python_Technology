import re
import csv

def format_string(string):
    string = re.sub(r'<[^>]+>', r'', string)
    string = re.sub(r'\b([01]?[0-9]|2[0-3])\.([0-5][0-9])\b', r'\1:\2', string)
    string = re.sub(r'\b(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+\d{4}\b', r'\4:\5:\6 \3/\2/\1', string)
    return string


file = input()
new_file = input()
highlight = input()

writer = csv.writer(open(new_file, 'w'))
reader = csv.reader(open(file, 'r', encoding='utf-8-sig'))

for row in reader:
    for i in range(len(row)):
        row[i] = format_string(row[i])
        for item in highlight.split(','):
            row[i] = re.sub(fr'(\b\w*{item}\w*\b)', lambda match: match.group(1).upper(), row[i], flags=re.IGNORECASE)

    writer.writerow(row)