import socket
import select

HEADER_LENGTH = 15

IP = "192.168.0.16"
PORT = 9001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
# List of sockets for select.select()
sockets_list = [server_socket]
# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_data(client_socket):
    try:
        # Reveive header containing data_length, data_type and the data itself
        data_header = client_socket.recv(HEADER_LENGTH)

        if not len(data_header):
            print("no data in header")
            return False
        
        # Convert header to int value
        data_length, data_type = data_header.decode("utf-8").split(' ')[:2]

        # Return an object of message header and message data
        return {'header': data_header, 'type': data_type, 'data': client_socket.recv(int(data_length))}
    except Exception as e:
        print(e)
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
            user = receive_data(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                print("No data from user")
                continue
            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(client_address[0], client_address[1], user['data'].decode('utf-8')))

        # else existing socket is sending a message
        else:

            # Receive message
            data = receive_data(notified_socket)

            if data is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received data from {user["data"].decode("utf-8")}: {data["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    client_socket.send(user['header'] + user['data'] + data['header'] + data['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]