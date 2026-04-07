import csv

filename = input()
headers = []
vacan = []

with open(filename, 'r', encoding='utf-8-sig') as f:
	reader = csv.reader(f)

	headers = next(reader)
	for line in reader:
		editedline = [ el for el in line if el != '']
		if len(editedline) >= len(headers) / 2:
			vacan.append(line)

print(headers)
print(vacan)