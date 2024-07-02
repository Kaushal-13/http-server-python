# Uncomment this to pass the first stage
import socket


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

        finally:
            print("Done")


if __name__ == "__main__":
    main()
