from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
import random


class Server:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._server = socket(AF_INET, SOCK_STREAM)
        self._reg_advisees = []  # Advisees connected to the server
        self._client_info = {}  # {client_socket: role}
        self._questions = {}  # {advisee: question}
        self._sem = Lock()  # Semaphore prevents race cond between advisors

    def start_server(self):
        """Starts the server and listens for clients trying to connect"""
        self._server.bind((self._host, self._port))
        self._server.listen()
        print(f"Server is running on {self._server.getsockname()}")
        self._listen_for_connections()

    def _listen_for_connections(self):
        """Accepts clients and starts a thread to serve the client"""
        while True:
            client_socket, address = self._server.accept()
            print(f"Accepted connection from {address}")
            thread = Thread(target=self._handle_client, args=(client_socket,))
            thread.start()

    def _handle_client(self, client_socket: socket):
        """Handles client logic"""
        self._assign_role(client_socket)
        while True:
            # If role is advisor, get question and send to advisor, then get advisor's answer and send to relevant
            # advisee
            if self._get_role(client_socket) == "Advisor":
                advisee, situation = self._get_advisee()
                client_socket.send(situation.encode())
                advice = client_socket.recv(1024).decode()
                advisee.send(advice.encode())
                self._cont(client_socket)

            # If client's role is advisee fetch their question and add them to the list of clients who sent questions
            elif self._get_role(client_socket) == "Advisee":
                situation = client_socket.recv(1024).decode()
                self._questions.update({client_socket: situation})

                self._cont(client_socket)

    def _get_role(self, client_socket: socket):
        """Gets a client's role"""
        return self._client_info.get(client_socket)

    def _get_advisee(self):
        """Finds the first question asked by an advisee and sends to advisor"""
        while not self._questions:
            continue
        advisee = list(self._questions.keys())[0]
        situation = self._questions.pop(advisee)
        self._reg_advisees.remove(advisee)
        return advisee, situation

    def _assign_role(self, client_socket: socket):
        """Assigns a random role to a client, assigns advisee if there are no registered advisees in the system"""
        role = random.choice(["Advisee", "Advisor"])
        if role == "Advisee":
            self._reg_advisees.append(client_socket)
            client_socket.send(role.encode())
        else:
            if len(self._reg_advisees) > 0:
                client_socket.send(role.encode())
            else:
                role = "Advisee"
                self._reg_advisees.append(client_socket)
                client_socket.send(role.encode())

        print(f"Assigning role \"{role}\" to {client_socket.getpeername()}...")
        self._client_info[client_socket] = role

    def _cont(self, client_socket):
        """Checks if a client wishes to continue"""
        continuing = client_socket.recv(1024).decode()
        self._client_info.pop(client_socket)
        if continuing.lower() == "y":
            self._handle_client(client_socket)
            return
        client_socket.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    server = Server(HOST, PORT)
    server.start_server()
