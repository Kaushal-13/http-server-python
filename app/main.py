# Uncomment this to pass the first stage
import socket
import threading
import os
import argparse


ok_response = 'HTTP/1.1 200 OK\r\n\r\n'
ok_response_pre = 'HTTP/1.1 200 OK\r\n'

error_response = 'HTTP/1.1 404 Not Found\r\n\r\n'


def echo_helper(string, content_type="text/plain"):
    return f'Content-Type: {content_type}\r\nContent-Length: {len(string)}\r\n\r\n{string}'


def file_helper(string, file_size):
    content_type = "application/octet-stream"
    return f'Content-Type: {content_type}\r\nContent-Length: {file_size}\r\n\r\n{string}'


acceptable_paths = ['/echo', '/user-agent', '/files', '/']


def handle_client(client_socket):
    try:

        print(f'Connection from {client_socket.getpeername()}')
        data = client_socket.recv(1024)
        if not data:
            return
        read_data = data.decode().strip("\r\n")
        print(read_data)
        read_data = read_data.split(' ')
        print(read_data)
        action_name = read_data[1]
        print(action_name)

        if action_name == "/":
            client_socket.send(ok_response.encode())
        else:
            for path in acceptable_paths:
                if action_name.startswith(path):
                    if path == "/echo":
                        st = action_name.split('/')[2]
                        st = echo_helper(st)
                        st = ok_response_pre + st
                        print(st)
                        client_socket.send(st.encode())
                        break
                    elif path == "/user-agent":
                        st = read_data[-1]
                        print(st)
                        st = echo_helper(st)
                        st = ok_response_pre + st
                        print(st)
                        client_socket.send(st.encode())
                        break
                    elif path == "/files":
                        global base_directory
                        directory = base_directory
                        message = error_response

                        try:
                            file_name = action_name.split('/')[2]
                            my_path = directory + "/" + file_name
                            file_size = os.path.getsize(my_path)
                            with open(my_path, 'r') as file:
                                file_content = file.read()
                                print("File Content")
                                print(file_content)
                            my_string = file_helper(
                                file_name, file_size=file_size)
                            message = ok_response_pre + my_string
                            client_socket.send(message.encode)

                            print(f"Size of the file is: {file_size} bytes")
                        except FileNotFoundError:
                            print(f"File not found: {st}")
            else:
                client_socket.send(error_response.encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print("Connection closed")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument("--directory", type=str, required=False,
                        help="Directory where files are stored")
    args = parser.parse_args()

    global base_directory
    base_directory = args.directory

    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()
    print("Server is listening on localhost:4221")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":

    main()
