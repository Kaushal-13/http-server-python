# Uncomment this to pass the first stage
import socket


ok_response = 'HTTP/1.1 200 OK\r\n\r\n'
ok_response_pre = 'HTTP/1.1 200 OK\r\n'

error_response = 'HTTP/1.1 404 Not Found\r\n\r\n'


def echo_helper(string):
    return f'Content-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}'


acceptable_paths = ['/echo', '/user-agent', '/']


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    while True:
        server_socket = socket.create_server(
            ("localhost", 4221), reuse_port=True)
        server_socket.listen()
       # wait for client

        try:
            client, addr = server_socket.accept()
            print(f'Connection from {client},{addr}')
            data = client.recv(1024)
            read_data = data.decode()
            read_data = read_data.strip("\r\n")
            print(read_data)
            read_data = read_data.split(' ')
            print(read_data)
            action_name = read_data[1]
            print(action_name)
            if (action_name == "/"):
                client.send(ok_response.encode())
            for paths in acceptable_paths:
                if (action_name.startswith(paths)):
                    if (paths == "/echo"):
                        st = action_name.split('/')[2]
                        st = echo_helper(st)
                        st = ok_response_pre + st
                        print(st)
                        client.send(st.encode())
                    elif (paths == '/user-agent'):
                        st = read_data[-1]
                        print(st)
                        st = echo_helper(st)
                        st = ok_response_pre + st
                        print(st)
                        client.send(st.encode())

            else:
                client.send(error_response.encode())

        finally:
            print("Done")
            client.close()


if __name__ == "__main__":

    main()
