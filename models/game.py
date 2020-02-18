import struct
import socket
import numpy as np

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

    def get_shape(self):
        return self._shape
        
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

    def send_name(self, name):
        msg_to_send = b'NME'
        msg_to_send += struct.pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)

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

    def update_map(self):
        upd_code = self._sock.recv(3).decode()
        assert upd_code == 'UPD'
        nb_changes = struct.unpack('B', self._sock.recv(1))[0]
        for i in range(nb_changes):
            x_case = struct.unpack('B', self._sock.recv(1))[0]
            y_case = struct.unpack('B', self._sock.recv(1))[0]
            nb_humans = struct.unpack('B', self._sock.recv(1))[0]
            nb_vampires = struct.unpack('B', self._sock.recv(1))[0]
            nb_werewolves = struct.unpack('B', self._sock.recv(1))[0]
            self._map[y_case, x_case] = [nb_humans, nb_vampires, nb_werewolves]

    def _load_set(self):
        set_code = self._sock.recv(3).decode()
        assert set_code == 'SET'
        n = struct.unpack('B', self._sock.recv(1))[0]
        m = struct.unpack('B', self._sock.recv(1))[0]
        self._shape = n, m

    def _load_humans(self):
        human_code = self._sock.recv(3).decode()
        assert human_code == 'HUM'
        n_maison = struct.unpack('B', self._sock.recv(1))[0]
        list_coordonnees = []
        for _ in range(n_maison):
            x = struct.unpack('B', self._sock.recv(1))[0]
            y = struct.unpack('B', self._sock.recv(1))[0]
            list_coordonnees.append((x, y))
        self._houses = list_coordonnees

    def _load_home(self):
        home_code = self._sock.recv(3).decode()
        assert home_code == 'HME'
        x_depart = struct.unpack('B', self._sock.recv(1))[0]
        y_depart = struct.unpack('B', self._sock.recv(1))[0]
        self._depart = y_depart, x_depart

    def _load_map(self):
        map_code = self._sock.recv(3).decode()
        assert map_code == 'MAP'
        n_map = struct.unpack('B', self._sock.recv(1))[0]
        self._map = np.zeros((*self._shape,3))
        for _ in range(n_map):
            x_case = struct.unpack('B', self._sock.recv(1))[0]
            y_case = struct.unpack('B', self._sock.recv(1))[0]
            nb_humans = struct.unpack('B', self._sock.recv(1))[0]
            nb_vampires = struct.unpack('B', self._sock.recv(1))[0]
            nb_werewolves = struct.unpack('B', self._sock.recv(1))[0]
            print("Sur la case {}, il y a {} humain(s), {} vampire(s) et {} loups garous".format((x_case, y_case), nb_humans, nb_vampires, nb_werewolves))
            self._map[y_case, x_case] = [nb_humans, nb_vampires, nb_werewolves]

    def _load_initial_parameters(self):
        # Getting the information about the map (SET)
        self._load_set()
        # Récupération des humains à setup sur la grille
        self._load_humans()
        # Case de départ
        self._load_home()
        # Get Map
        self._load_map()