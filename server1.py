import socket
from _thread import *


def client_thread(connection, player):
    connection.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break

            print(f"Recieved: {reply}")
            print(f"Sedning: {reply}")
            connection.sendall(str.encode(reply))

        except:
            print("Failed to estabilsh client thread connection")

    connection.close()



def main():
    server_ip = "192.168.32.1"
    port = 9001

    # Initialize socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to associate socket object with server ip and port
    try:
        s.bind((server_ip, port))
    except socket.error as e:
        str(e)

    # Listen for incomming connections
    s.listen(2)
    print("Server Started. Awaiting connection...")

    player = 0
    while True:
        connection, address = s.accept()
        print("Connected to: ", address)

        start_new_thread(client_thread, (connection, player))
        player += 1

        



if __name__ == "__main__":
    main()