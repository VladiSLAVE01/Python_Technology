import socket
import json
import pandas as pd
import threading


def get_website(dataframe, organization_name):
	return dataframe[dataframe['Name'] == organization_name]['Website'].values[0]


def get_country(dataframe, organization_name):
	return dataframe[dataframe['Name'] == organization_name]['Country'].values[0]


def get_number_of_employees(dataframe, organization_name):
	return str(dataframe[dataframe['Name'] == organization_name]['Number of employees'].values[0])


def get_description(dataframe, organization_name):
	return dataframe[dataframe['Name'] == organization_name]['Description'].values[0]


def handle_client(connection, dataframe):
	while True:
		received_data = connection.recv(1024).decode()

		if received_data == 'exit':
			connection.close()
			break

		if len(received_data) == 0:
			connection.close()
			break

		parsed_data = json.loads(received_data)
		response_data = None

		if parsed_data['operation'] == 'get_website':
			response_data = get_website(dataframe, parsed_data['name'])

		if parsed_data['operation'] == 'get_country':
			response_data = get_country(dataframe, parsed_data['name'])

		if parsed_data['operation'] == 'get_number_of_employees':
			response_data = get_number_of_employees(dataframe, parsed_data['name'])

		if parsed_data['operation'] == 'get_description':
			response_data = get_description(dataframe, parsed_data['name'])

		connection.send(json.dumps({"result": response_data}).encode())


def start_server():
	data_frame = pd.read_csv("organizations.csv")
	server_host = "127.0.0.32"
	server_port = 12345

	server_socket = socket.socket()
	server_socket.bind((server_host, server_port))
	server_socket.listen(5)

	while True:
		client_connection, client_address = server_socket.accept()
		worker_thread = threading.Thread(target=handle_client, args=(client_connection, data_frame)).start()


start_server()