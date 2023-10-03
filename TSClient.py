import sys
from socket import *
import time

"""
This class initializes a local client that attempts to establish
a TCP connection with a specified server. It runs the NTP, calculates 
offset and delay, and adjusts local clock. NOTE: this class adjusting a
local clock variable, not the actual machine clock.

Usage:
python TSClient.py [serverName]
"""


class TSClient:

    def __init__(self, serverName):
        self.serverName = serverName
        self.serverPort = 10085
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

        # local time after it has been adjusted to match the server
        self.synchronized_local_time = None

        # initializing timestamps
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None

    def send_request(self):
        # t1 measured at the time the request is sent
        self.t1 = time.time()

        self.clientSocket.send(''.encode())
        server_times = self.clientSocket.recv(1024).decode().split(',')

        # t4 measured at the time the response is received
        self.t4 = time.time()

        # parse t2 and t3 from response
        self.t2 = float(server_times[0])
        self.t3 = float(server_times[1])

        self.clientSocket.close()

    def time_sync(self):
        delay = self.calculate_delay()
        offset = self.calculate_offset()

        self.adjust_client_clock(offset)
        self.output_results(delay)

    def calculate_delay(self):
        return ((self.t4 - self.t1) - (self.t3 - self.t2)) * 1000

    def calculate_offset(self):
        return (((self.t2 - self.t1) + (self.t3 - self.t4)) / 2) * 1000

    # sets our local time to match server time
    def adjust_client_clock(self, offset):
        self.synchronized_local_time = time.time() + offset

    def output_results(self, delay):
        print(f'REMOTE_TIME {int(self.synchronized_local_time)}')
        print(f'LOCAL_TIME {int(time.time())}', )
        print(f'RTT_ESTIMATE {int(delay)}')


if __name__ == "__main__":
    try:
        server_name = sys.argv[1]
    except IndexError:
        server_name = 'localhost'

    client = TSClient(server_name)
    client.send_request()
    client.time_sync()
