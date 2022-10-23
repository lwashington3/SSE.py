i = -1


def default_incrementer():
	global i
	i += 1
	return i


def create_event_str(data:dict|str, event_type="event", _id=None) -> str:
	"""
	Parse the given data into the default SSE format.

	:param dict | str data: The data to be sent. If the data object is a dictionary, it will be treated like a JSON object would be.
	:param str event_type:
	:param int | None _id: The id of the event. This should be left default unless an outside incrementer is keeping track.
	:return:
	"""
	_id = default_incrementer() if _id is None else _id

	if isinstance(data, dict):
		from json import dumps
		data = dumps(data)
	elif not isinstance(data, str):
		data = str(data)

	return f"id: {id}\nevent: {event_type}\ndata: {data}\n\n"


def stop_event_str() -> str:
	return create_event_str("Close listening", "close", -1)


def send_debug(host:str, port:int):
	from socket import socket
	server_socket = socket()
	server_socket.bind((host, port))

	# Tells the socket how many clients can listen simultaneously
	server_socket.listen(2)
	conn, address = server_socket.accept()
	print(f"Connection from: {address}")
	while True:
		data = input("Input something to send >> ")
		stop = False
		if not data:
			stop = True
			data = stop_event_str()
		conn.send(create_event_str(data).encode())
		if stop:
			break

	conn.close()
