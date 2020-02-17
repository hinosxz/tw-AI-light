from client import *
import struct
import socket
import numpy as np


def load_map(L,shape):
    L = L[3:]
    nb_element = L.pop(0)
    M = np.zeros((*shape,3))
    for i in range(0,len(L),5):
        M[L[i+1],L[i]] = L[i+2:i+5]
    return nb_element,M

def update_map(map,L,is_vampr):
    L = L[3:]
    nb_changes = L.pop(0)
    for i in range(0,len(L),5):
        map[L[i+3]-1,L[i+4]-1][is_vampr] = map[L[i]-1,L[i+1]-1][is_vampr] + L[i+2]
        map[L[i]-1,L[i+1]-1][is_vampr] -= L[i+2]
    return map

def load_static(L):
    # shape
    L = L[3:]
    shape = L.pop(0), L.pop(0)
    # houses
    L = L[3:]
    nb_house = L.pop(0)
    houses_dict = {}
    for i in range(nb_house):
        houses_dict[i] = L.pop(0), L.pop(0)
        houses_dict[i] = houses_dict[i][1], houses_dict[i][0]
    # point of departure
    L = L[3:]
    depart = L.pop(0), L.pop(0)
    depart = depart[1],depart[0]

    nb_element, map = None, None
    if L!=[]:
        nb_element, map = load_map(L, shape)
    return nb_element, map, shape, houses_dict, depart


class Game:

    def __init__(self, hote="127.0.0.1", port=5555):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((hote, port))
        self._shape = None
        self._houses = None
        self._depart = None
        self._map = None
        self._type = None

    def get_humans_dict(self):
        humans_dict = {}
        for i, row in enumerate(self._map):
            for j, cell in enumerate(row):
                if cell[0] != 0:
                    humans_dict[(i,j)] = cell[0]
        print(humans_dict)
        return humans_dict

    def assign_type(self, type):
        self._type = type

    def get_depart(self):
        return self._depart  
        
    def get_map(self):
        return self._map

    def get_opponent_position(self):
        opponent_dict = {}
        for i,row in enumerate(self._map):
            for j,cell in enumerate(row):
                if self._type == 'vampire':
                    if cell[1] != 0:
                        opponent_dict[(i,j)] = cell[1]
                elif self._type == 'wolf':
                    if cell[2] != 0:
                        opponent_dict[(i,j)] = cell[2]
        return opponent_dict

    def send_names(self, name):
        msg_to_send = b'NME'
        msg_to_send += struct.pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)
        msg_recu = self.receive_message()
        _, self._map, self._shape, self._houses, self._depart = load_static(msg_recu)

    def send_move(self, moves_dict, type):
        msg_to_send = b'MOV'
        msg_to_send += struct.pack('B', len(moves_dict.keys()))
        for key in moves_dict.keys():
            to_pos_x, to_pos_y = moves_dict[key]['to_position']
            from_pos_x, from_pos_y = moves_dict[key]['from_position']
            if type == 'vampire':
                self._map[to_pos_x, to_pos_y][1] = self._map[from_pos_x, from_pos_y][1] - moves_dict[key]['number']
                self._map[from_pos_x, from_pos_y][1] -= moves_dict[key]['number']
            if type == 'wolf':
                self._map[to_pos_x, to_pos_y][2] = self._map[from_pos_x, from_pos_y][2] - moves_dict[key]['number']
                self._map[from_pos_x, from_pos_y][2] -= moves_dict[key]['number']
            msg_to_send += struct.pack('B', int(moves_dict[key]['from_position'][1]))
            msg_to_send += struct.pack('B', int(moves_dict[key]['from_position'][0]))
            msg_to_send += struct.pack('B', int(moves_dict[key]['number']))
            msg_to_send += struct.pack('B', int(moves_dict[key]['to_position'][1]))
            msg_to_send += struct.pack('B', int(moves_dict[key]['to_position'][0]))
        self._sock.send(msg_to_send)

    def receive_message(self):
        ## TO DO put the end and things like that here
        return list(self._sock.recv(1024))

    def update_map(self):
        msg_recu = self.receive_message()
        if self._type == 'wolf':
            self._map = update_map(self._map, msg_recu,2)
        elif self._type == 'vampire':
            self._map = update_map(self._map, msg_recu,1)


    
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



