import socket
import csv


def load_organizations():
	organizations_dict = {}

	with open('organizations.csv', 'r', encoding='utf-8') as csvfile:
		csv_reader = csv.reader(csvfile)
		headers = next(csv_reader)

		name_index = headers.index('Name')
		website_index = headers.index('Website')
		country_index = headers.index('Country')

		for row in csv_reader:
			org_name = row[name_index]
			website = row[website_index]
			country = row[country_index]
			organizations_dict[org_name] = {'website': website, 'country': country}

	return organizations_dict


def create_server_socket():
	host = "127.0.0.32"
	port = 12345

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((host, port))
	server_socket.listen(1)

	return server_socket


def process_client_message(message, organizations_dict):
	if message == "exit":
		return "Соединение закрыто"

	if message in organizations_dict:
		org_data = organizations_dict[message]
		return f"Сайт: {org_data['website']}. Страна: {org_data['country']}"
	else:
		return f"Организация '{message}' не найдена"


def handle_client_connection(client_socket, organizations_dict):
	while True:
		message = client_socket.recv(1024).decode().strip()

		if not message:
			break

		response = process_client_message(message, organizations_dict)
		client_socket.sendall(response.encode())

		if message == "exit":
			break

	client_socket.close()


def start_server():
	organizations_dict = load_organizations()
	server_socket = create_server_socket()

	while True:
		client_socket, client_address = server_socket.accept()
		handle_client_connection(client_socket, organizations_dict)


if __name__ == "__main__":
	start_server()