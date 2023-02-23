import socket as sock
import threading
import random


class Server:
    available_roles = ["Advisor", "Advisee"]

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self._clients = []
        self._free_clients = []
        self._client_pairs = {}  # {advisor: advisee}
        self._roles = {}         # {client_socket: role}
        self._questions = {}     # {advisee: question}

    def start_server(self):
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print(f"Server is running on {self._server_socket.getsockname()}")
        self._listen_for_connections()

    def _listen_for_connections(self):
        while True:
            client_socket, address = self._server_socket.accept()
            self._clients.append(client_socket)
            self._free_clients.append(client_socket)
            print(f"Accepted connection from {address}")
            thread = threading.Thread(target=self._handle_client, args=(client_socket,))
            thread.start()

    def _handle_client(self, client_socket: sock.socket):
        self._assign_role(client_socket)
        self._pair_clients(client_socket)

        if self._get_role(client_socket) == "Advisor":
            # TODO implement advisor behaviour
            while not self._questions.get(self._client_pairs.get(client_socket)):
                continue
            situation = self._questions.get(self._client_pairs.get(client_socket))
            client_socket.send(f"Situation requiring advice: {situation}".encode())
            advice = self._server_socket.recv(1024).decode()
            self._client_pairs.get(client_socket).send(f"Advice sent by advisor: {advice}".encode())

        elif self._get_role(client_socket) == "Advisee":
            # TODO implement advisee behaviour
            client_socket.send("What do you need advice about? \n".encode())
            situation = self._server_socket.recv(1024).decode()
            self._questions.update({client_socket: situation})

    def _get_role(self, client_socket: sock.socket):
        return self._roles.get(client_socket)

    def _assign_role(self, client_socket: sock.socket):
        role = random.choice(self.available_roles)
        print(f"Assigning role \"{role}\" to {client_socket.getpeername()}...")
        client_socket.send(role.encode())
        self._roles.update({client_socket: role})

    def _pair_clients(self, client_socket: sock.socket):

        if self._get_role(client_socket) == "Advisor":
            self._client_pairs[client_socket] = ""
            client_socket.send("Waiting for an advisee to connect you too...".encode())

            while not self._client_pairs.get(client_socket):
                # Wait for an advisee to connect
                continue

            client_socket.send("An advisee has connected to you".encode())

        elif self._get_role(client_socket) == "Advisee":
            client_socket.send("Waiting for a free advisor to connect to...".encode())

            while all(self._client_pairs.values()):
                # Wait for a free advisor
                continue

            for i in self._client_pairs.keys():
                if not self._client_pairs[i]:
                    self._client_pairs[i] = client_socket
                    client_socket.send("Connected you to an advisor".encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    server = Server(HOST, PORT)
    server.start_server()
