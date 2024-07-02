# Uncomment this to pass the first stage
import socket
from io import BytesIO


ok_response = 'HTTP/1.1 200 OK\r\n\r\n'
error_response = 'HTTP/1.1 404 Not Found\r\n\r\n'


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    while True:
        server_socket = socket.create_server(
            ("localhost", 4221), reuse_port=True)
        client, addr = server_socket.accept()  # wait for client

        try:

            print(f'Connection from {client},{addr}')
            data = client.recv(1024)
            print(data)
            read_data = data.decode()
            print([read_data])
        finally:
            print("Done")
            client.close()


if __name__ == "__main__":
    main()
