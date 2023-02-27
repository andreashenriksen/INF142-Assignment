import socket as sock


class Client:

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._role = ""
        self._client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connect_to_server(self):
        self._client_socket.connect((self._host, self._port))
        self._role = self._client_socket.recv(1024).decode()
        print(f"Assigned role \"{self._role}\" by server")
        self._start_session()

    def _start_session(self):

        if self._role == "Advisor":
            self._receive_partner()
            situation = self._client_socket.recv(1024).decode()  # Receive a situation to give advice to
            print(situation)
            advice = input()
            self._client_socket.send(advice.encode())

        elif self._role == "Advisee":
            self._receive_partner()
            print(self._client_socket.recv(1024).decode())  # Server asking for your situation
            situation = input()
            self._client_socket.send(situation.encode())
            print("Waiting for advice...")
            print(self._client_socket.recv(1024).decode())  # Waiting for advice...

    def _receive_partner(self):
        print(self._client_socket.recv(1024).decode())  # Waiting for connection
        print(self._client_socket.recv(1024).decode())  # Connection established to 2nd client


if __name__ == "__main__":
    SERVER_HOST, SERVER_PORT = "localhost", 5000

    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect_to_server()
