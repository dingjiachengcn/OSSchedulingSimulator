import random
import time
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
END_MESSAGE = "END"


def send_process_info(client_socket):
    pid = random.randint(1, 100)
    burst_time = random.randint(1, 5)
    process_info = f"{pid} {burst_time}"
    client_socket.send(process_info.encode())
    logger.info(f"Sent process info: {process_info}")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    logger.info(f"Waiting for incoming connections on {SERVER_IP}:{SERVER_PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        logger.info(f"Accepted connection from {client_address}")
        start_time = time.time()

        while time.time() - start_time < 60:
            send_process_info(client_socket)
            time.sleep(random.uniform(0.1, 1.0))

        # Send "END" message to signal the end of input
        client_socket.send(END_MESSAGE.encode())
        client_socket.close()
        logger.info("Input generation completed.")


if __name__ == "__main__":
    main()
