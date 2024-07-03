# Uncomment this to pass the first stage
import socket


ok_response = 'HTTP/1.1 200 OK\r\n\r\n'
ok_response_pre = 'HTTP/1.1 200 OK\r\n'

error_response = 'HTTP/1.1 404 Not Found\r\n\r\n'


def echo_helper(string):
    return f'Content-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}'


acceptable_paths = ['/echo', '/user-agent', '/']


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
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
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
        # client.close()


if __name__ == "__main__":

    main()
