import socket
import sys
import errno
import random
import pygame


class Network:
    def __init__(self, screen):
        pygame.init()
        self.IP = "192.168.0.16"
        self.PORT = 9001
        self.HEADER_LENGTH = 15
        self.SCREEN = screen
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = f"TESTING{random.randint(1, 10)}"
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)

        self.messages = []
        self.hits = []
        self.enemy_hits = []
        self.ship_locations = {}
        self.enemy_ship_locations = {}

        self.init()
 
    def init(self):
        self.send(self.username)

    def send(self, data, data_type="{USR}"):
        """Sending data to the server in the form of {data_header}{data}"""
        data = str(data).encode("utf-8")
        header_content = f"{len(data)} {data_type}"
        data_header = f"{header_content:<{self.HEADER_LENGTH}}".encode("utf-8") 
        self.client_socket.send(data_header + data)
        print(f"Sending data: {data_header + data}")

    def receive(self):
        data_header = self.client_socket.recv(self.HEADER_LENGTH)
        if not len(data_header):
            print("Connection closed by the server")
            sys.exit() 
        data_length, data_type = data_header.decode("utf-8").split(' ')[:2]
        data = self.client_socket.recv(int(data_length)).decode("utf-8")     # Receive remaining data
        return data_header, data_type, data
    
    def check_hit(self, data):
        if data in self.ship_locations:
            return True
        return False
    
    def to_tuple(self, string_tuple):
        x, y = string_tuple[1:len(string_tuple)-1].strip().split(",")
        return (int(x), int(y))
    
    def display_chat_text(self, username, data):
        pass

    def loop(self):
        """Looping over received messages"""
        if self.hits:
            hit = self.hits.pop()
            self.send(hit, data_type="{HIT}")

        if self.messages:
            message = self.messages.pop()
            self.send(message, data_type="{MSG}")

        while True:
            try:
                # Data is received in format {username_header}{username}{data_header}{data}
                _,    _,  username = self.receive()
                _, data_type, data = self.receive()
                
                if data_type == "{HIT}":
                    data = self.to_tuple(data)
                    print("THIS IS A HIT")
                    if self.check_hit(data):
                        if self.ship_locations[data]["hits"] + 1 == self.ship_locations[data]["max_hits"]:
                            del self.ship_locations[data]
                            self.enemy_hits.append(data)
                            print(f"{username} sunk his enemy's ship")
                        else:
                            self.ship_locations[data]["hits"] += 1
                            print(f"{username} hit his enemy's ship")
                    else:
                        self.enemy_hits.append(data)
                        print(f"{username} missed the enemy ship")
                else:
                    print(f"{username}:  {data}")
                print("hello")

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error: ", str(e))
                    sys.exit()
                break
            except Exception as e:
                print("Error: ", str(e))
                sys.exit()