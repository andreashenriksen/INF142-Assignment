import socket as sock
import threading
import random


class Server:

    available_roles = ["Advisor", "Advisee"]

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self._clients = []
        self._roles = {}
        self._situation = ""

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server is running on {self.server_socket.getsockname()}")
        self._listen_for_connections()

    def _listen_for_connections(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self._clients.append(client_socket)
            print(f"Accepted connection from {address}")
            thread = threading.Thread(target=self._handle_client, args=(client_socket,))
            thread.start()

    def _handle_client(self, client_socket: sock.socket):
        self._assign_role(client_socket)

    def _get_role(self, client_socket: sock.socket):
        return self._roles.get(client_socket)

    def _assign_role(self, client_socket: sock.socket):
        role = random.choice(self.available_roles)
        print(f"Assigning role \"{role}\" to {client_socket.getpeername()}...")
        client_socket.send(role.encode())
        self._roles.update({client_socket: role})


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    server = Server(HOST, PORT)
    server.start_server()
