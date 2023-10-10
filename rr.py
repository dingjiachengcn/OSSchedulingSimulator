import socket
import struct
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
MAX_BUFFER_SIZE = 1024
TIME_QUANTUM = 2  # Adjust the time quantum as needed

# Class to represent a process
class Process:
    def __init__(self, pid, burst_time, remaining_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = remaining_time

# Class for the ready queue data structure
class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, process):
        self.data.append(process)

    def dequeue(self):
        if len(self.data) > 0:
            return self.data.pop(0)
        else:
            return None

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a socket
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        print("Connection failed:", e)
        exit(1)

    print("Connected to the server")
    ready_queue = Queue()
    current_time = 0

    while True:
        # Receive process information from the server
        process_info = client_socket.recv(MAX_BUFFER_SIZE).decode()

        # Break if no information received or if END message is received
        if not process_info or process_info == "END":
            break

        pid, burst_time = map(int, process_info.split())
        process = Process(pid, burst_time, burst_time)
        ready_queue.enqueue(process)

        # Check if there are processes in the queue and execute
        while len(ready_queue.data) > 0:
            current_process = ready_queue.dequeue()

            # If process can be completed within the time quantum
            if current_process.remaining_time <= TIME_QUANTUM:
                print(
                    f"Process {current_process.pid} is running from time {current_time} to {current_time + current_process.remaining_time}")
                current_time += current_process.remaining_time
            else:
                print(
                    f"Process {current_process.pid} is running from time {current_time} to {current_time + TIME_QUANTUM}")
                current_time += TIME_QUANTUM
                current_process.remaining_time -= TIME_QUANTUM
                ready_queue.enqueue(current_process)

    client_socket.close()

if __name__ == "__main__":
    main()
