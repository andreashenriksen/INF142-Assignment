import socket as sock


class Client:

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._role = ""
        self._client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect_to_server(self):
        self._client_socket.connect((self._host, self._port))
        server_message = self._client_socket.recv(1024).decode()
        print(f"Assigned role \"{server_message}\" by server")


if __name__ == "__main__":
    SERVER_HOST, SERVER_PORT = "localhost", 5000

    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect_to_server()
