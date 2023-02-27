from socket import socket, AF_INET, SOCK_STREAM


class Client:

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self._role = ""
        self._client = socket(AF_INET, SOCK_STREAM)

    def connect_to_server(self):
        self._client.connect((self._host, self._port))
        print(f"Connected to {self._host} on {self._port}")
        self._start_session()

    def _start_session(self):
        """Receives role from server and acts according to role given"""
        self._role = self._client.recv(1024).decode()
        print(f"Assigned role \"{self._role}\" by server")

        if self._role == "Advisor":
            while True:
                situation = self._client.recv(1024).decode()  # Receive a situation to give advice to
                print(f"Someone needs advice on this situation: {situation}")
                advice = input("Give your advice: ")
                self._client.send(advice.encode())
                self._continue()
                return

        elif self._role == "Advisee":
            while True:
                print("What do you need advice on?")
                situation = input("Input your situation: ")
                self._client.send(situation.encode())
                print("Waiting for advice...")
                print(self._client.recv(1024).decode())  # Waiting for advice...
                self._continue()
                return

    def _continue(self):
        """Asks user if they want to continue"""
        print("Do you want to continue?\n")
        continuing = input("Answer \"y\" or \"n\"?: ")
        self._client.send(continuing.encode())
        if continuing == "y":
            self._start_session()
            return
        self._client.close()


if __name__ == "__main__":
    SERVER_HOST, SERVER_PORT = "localhost", 5000

    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect_to_server()
