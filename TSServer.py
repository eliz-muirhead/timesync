import socket
import time

"""
This class initializes a local server that can establish
a TCP connections with clients. It listens for incoming requests,
timestamps the reception of the request, then timestamps and
sends responds to clients.

Usage:
python TSServer.py
"""


class TSServer:

    def __init__(self):
        self.serverPort = 10085
        self.my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_server_socket.bind(('', self.serverPort))
        self.my_server_socket.listen(1)

    def send_response(self):
        connection_socket, addr = self.my_server_socket.accept()
        # t2 measured at the time the request is received
        t2 = time.time().__str__()

        # t3 measured at the same the response is sent
        connection_socket.send(f'{t2},{time.time().__str__()}'.encode())
        connection_socket.close()


def main():
    server = TSServer()
    while True:
        server.send_response()


main()
