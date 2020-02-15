from client import *
import struct
import socket

class Game:

    def __init__(self, hote="127.0.0.1", port=5555):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((hote, port))


    def send_names(self, name):
        msg_to_send = b'NME'
        msg_to_send += struct.pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)

    def load_static():
        # Receive start message
        msg_recu = self.receive_message()
        # shape
        L = msg_recu[3:]
        shape = L.pop(0), L.pop(0)
        # need to inverse the two positions
        shape = shape[1],shape[0]
        # houses
        L = L[3:]
        nb_house = L.pop(0)
        houses_dict = {}
        for i in range(nb_house):
            houses_dict[i] = L.pop(0), L.pop(0)
            houses_dict[i] = houses_dict[i][1],houses_dict[i][0]
        # point of departure
        L = L[3:]
        depart = L.pop(0), L.pop(0)
        depart = depart[1], depart[0]
        # Probleme Load Map
        return L, shape, houses_dict, depart


    def receive_message():
        return list(self._sock.recv(1024)))


    
class Command:
    def __init__(self):
        pass

# class MOV(Command):
#     def __init__(self, sock, Species, **kwargs):
#         if len(kwargs)==0:
#             raise ValueError('You must move at least one group')
#         msg_to_send =  b'MOV'
#         for number in kwargs.keys():
#             for group in Species.groups():
#                 if number == group.get_size():
#                     try: 
#                         group.move(kwargs[number])
#                     except:
#                         pass
#                 elif number 
#         sock.send(msg_to_send)



