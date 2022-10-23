def decode_event_str(event:str, leave_as_string=False) -> tuple[str, str, str]:
	"""

	:param str event:
	:param bool leave_as_string: If the function should try converting JSON objects into dictionaries or if the should stay as strings.
	:return:
	"""
	from re import search
	from json import loads
	from json.decoder import JSONDecodeError

	match = search("id: (.+)\nevent: (.+)\ndata: (.+)\n\n\0?\r\n", event)
	if match is None:
		print(f"|{repr(event)}|")
		# raise ValueError(f"The given event string did not match the standard for events: \"{event}\".")
	data = match.group(3)

	if not leave_as_string:
		try:
			data = loads(data)
		except JSONDecodeError:
			pass
	return match.group(1), match.group(2), data


def listen_debug(host:str, port:int):
	def _interface(_id:str, event_type:str, message:str) -> bool:
		if event_type == "close" or _id == -1:
			return False
		print(message)
		return True
	listen_interface(host, port, _interface)


def listen_interface(host:str, port:int, interface):
	"""

	:param str host: The host
	:param int port: The port number
	:param function interface: An interface that takes in three string parameters, and returns a boolean where returning False closes the connection.
	"""
	from socket import socket, AF_INET, SOCK_STREAM
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((host, port))
	headers = f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
	client_socket.send(headers.encode())  # Sends the HTTP request.
	response = client_socket.recv(1024).decode()  # TODO: Check response to make sure everything is okay.
	print(f"Response from server: {response}")

	while True:
		data = client_socket.recv(1024).decode()
		if not data:
			break
		_id, event_type, message = decode_event_str(data)
		if not interface(_id, event_type, message):
			break

	client_socket.close()
