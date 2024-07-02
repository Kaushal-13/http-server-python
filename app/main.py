# Uncomment this to pass the first stage
import socket


ok_response = 'HTTP/1.1 200 OK\r\n'
error_response = 'HTTP/1.1 404 Not Found\r\n\r\n'


def echo_helper(string):
    return f'Content-Type: text/plain\r\n Content-Length: {len(string)} \r\n\r\n {string}'


acceptable_paths = ['/']


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    while True:
        server_socket = socket.create_server(
            ("localhost", 4221), reuse_port=True)
        client, addr = server_socket.accept()  # wait for client

        try:

            print(f'Connection from {client},{addr}')
            data = client.recv(1024)
            print(data)
            read_data = data.decode()
            print(read_data)
            read_data = read_data.strip("/r/n")
            read_data = read_data.split(' ')
            file_name = read_data[1]
            err = False
            comms = file_name.split('/')
            if (comms[1] == 'echo'):
                st = comms[2]
                st = echo_helper(st)
                st = ok_response + st
                print(st)
                client.send(st.encode())
            else:
                client.send(error_response.encode())

        finally:
            print("Done")
            client.close()


if __name__ == "__main__":
    main()
