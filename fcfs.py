import socket
import struct
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
MAX_BUFFER_SIZE = 1024

# Struct to represent a process
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

# Queue data structure
class Queue:
    def __init__(self, size):
        self.data = [None] * size
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, process):
        if self.size < MAX_BUFFER_SIZE:
            self.rear = (self.rear + 1) % MAX_BUFFER_SIZE
            self.data[self.rear] = process
            self.size += 1

    def dequeue(self):
        if self.size > 0:
            process = self.data[self.front]
            self.front = (self.front + 1) % MAX_BUFFER_SIZE
            self.size -= 1
            return process
        else:
            # Handle empty queue (return a dummy process or exit)
            dummy = Process(-1, 0, 0)
            return dummy

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a socket
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        print("Connection failed:", e)
        exit(1)

    print("Connected to the server")

    process_queue = Queue(MAX_BUFFER_SIZE)
    current_time = 0

    while True:
        # Receive process information from server
        process_info = client_socket.recv(MAX_BUFFER_SIZE).decode('utf-8')

        # Check for end message
        if process_info == "END":
            break

        pid, burst_time = map(int, process_info.split())
        process = Process(pid, current_time, burst_time)

        # Enqueue the received process
        process_queue.enqueue(process)

        # Dequeue and print the process in the queue
        while process_queue.size > 0:
            current_process = process_queue.dequeue()
            print(
                f"Received process info: PID={current_process.pid} Burst Time={current_process.burst_time} Arrival Time={current_process.arrival_time}")
            current_time += current_process.burst_time

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    main()
