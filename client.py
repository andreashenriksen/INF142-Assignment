import socket as sock


class Client:

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self._role = ""
        self.client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        server_message = self.client_socket.recv(1024).decode()
        print(f"Assigned role \"{server_message}\" by server")


if __name__ == "__main__":
    SERVER_HOST, SERVER_PORT = "localhost", 5000
    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect_to_server()
