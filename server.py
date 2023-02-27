from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
import random
import selectors


class Server:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._server = socket(AF_INET, SOCK_STREAM)
        self._advisee_queue = []
        self._client_info = {}  # {client_socket: role}
        self._questions = {}    # {advisee: question}
        self._lock = Lock()

    def start_server(self):
        self._server.bind((self._host, self._port))
        self._server.listen()
        print(f"Server is running on {self._server.getsockname()}")
        self._listen_for_connections()

    def _listen_for_connections(self):
        while True:
            client_socket, address = self._server.accept()
            print(f"Accepted connection from {address}")
            thread = threading.Thread(target=self._handle_client, args=(client_socket,))
            thread.start()

    def _handle_client(self, client_socket: socket):
        self._assign_role(client_socket)
        while True:
            if self._get_role(client_socket) == "Advisor":
                advisee, situation = self._get_advisee()
                client_socket.send(situation.encode())
                advice = client_socket.recv(1024).decode()
                advisee.send(advice.encode())

                continuing = client_socket.recv(1024).decode()
                self._client_info.pop(client_socket)
                if continuing.lower() == "yes":
                    self._handle_client(client_socket)
                    return
                client_socket.close()

            elif self._get_role(client_socket) == "Advisee":
                situation = client_socket.recv(1024).decode()
                self._questions.update({client_socket: situation})

                continuing = client_socket.recv(1024).decode()
                self._client_info.pop(client_socket)
                if continuing.lower() == "yes":
                    self._handle_client(client_socket)
                    return
                client_socket.close()

    def _get_role(self, client_socket: socket):
        return self._client_info.get(client_socket)

    def _get_advisee(self):
        while not self._questions:
            continue
        advisee = list(self._questions.keys())[0]
        situation = self._questions.pop(advisee)
        self._advisee_queue.remove(advisee)
        return advisee, situation

    def _assign_role(self, client_socket: socket):
        role = random.choice(["Advisee", "Advisor"])
        if role == "Advisee":
            self._advisee_queue.append(client_socket)
            client_socket.send(role.encode())
        else:
            if len(self._advisee_queue) > 0:
                client_socket.send(role.encode())
            else:
                role = "Advisee"
                self._advisee_queue.append(client_socket)
                client_socket.send(role.encode())

        print(f"Assigning role \"{role}\" to {client_socket.getpeername()}...")
        self._client_info[client_socket] = role


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    server = Server(HOST, PORT)
    server.start_server()
