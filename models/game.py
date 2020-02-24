import struct
import socket
import numpy as np


class Game:
    """
    This class creates an object that will interact with the server.

    When an instance is created, it initiates the connection and update the map of the field depending on the messages
    it receives.

    Parameters
    ----------
    host : string
        ip address on which the server is running
    port : integer
        port on which the server is listening
    """

    def __init__(self, host="127.0.0.1", port=5555):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))
        self._shape = None
        self._houses = None
        self._start = None
        self._map = None
        self._type = None
        self.is_running = True

    def get_humans_positions(self):
        humans_dict = {}
        for i, row in enumerate(self._map):
            for j, cell in enumerate(row):
                if cell[0] != 0:
                    humans_dict[(i, j)] = cell[0]
        return humans_dict

    def get_map(self):
        return self._map

    def get_opponent_positions(self):
        opponent_dict = {}
        for i, row in enumerate(self._map):
            for j, cell in enumerate(row):
                if self._type == "vampire":
                    if cell[1] != 0:
                        opponent_dict[(i, j)] = cell[1]
                elif self._type == "wolf":
                    if cell[2] != 0:
                        opponent_dict[(i, j)] = cell[2]
        return opponent_dict

    def get_start_info(self):
        start_cell = self._map[self._start]
        if start_cell[1] != 0:
            self._type = "vampire"
            total_nb = start_cell[1]
        else:
            self._type = "wolf"
            total_nb = start_cell[2]
        return self._type, total_nb, self._start

    def send_name_to_server(self, name):
        msg_to_send = b"NME"
        msg_to_send += struct.pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)

    def send_move(self, moves_list):
        msg_to_send = b"MOV"
        msg_to_send += struct.pack("B", len(moves_list))
        for move in moves_list:
            to_pos_x, to_pos_y = move["to_position"]
            from_pos_x, from_pos_y = move["from_position"]
            if type == "vampire":
                self._map[to_pos_x, to_pos_y][1] = (
                    self._map[from_pos_x, from_pos_y][1] - move["number"]
                )
                self._map[from_pos_x, from_pos_y][1] -= move["number"]
            elif type == "wolf":
                self._map[to_pos_x, to_pos_y][2] = (
                    self._map[from_pos_x, from_pos_y][2] - move["number"]
                )
                self._map[from_pos_x, from_pos_y][2] -= move["number"]
            msg_to_send += struct.pack("B", int(move["from_position"][1]))
            msg_to_send += struct.pack("B", int(move["from_position"][0]))
            msg_to_send += struct.pack("B", int(move["number"]))
            msg_to_send += struct.pack("B", int(move["to_position"][1]))
            msg_to_send += struct.pack("B", int(move["to_position"][0]))
        self._sock.send(msg_to_send)

    def update_map(self):
        upd_code = self._sock.recv(3).decode()
        try:
            assert upd_code == "UPD"
            nb_changes = struct.unpack("B", self._sock.recv(1))[0]
            self._update_cells(nb_changes)
        except AssertionError as e:
            self.end_game()

    def _update_cells(self, nb_changes):
        for i in range(nb_changes):
            x_case = struct.unpack("B", self._sock.recv(1))[0]
            y_case = struct.unpack("B", self._sock.recv(1))[0]
            nb_humans = struct.unpack("B", self._sock.recv(1))[0]
            nb_vampires = struct.unpack("B", self._sock.recv(1))[0]
            nb_werewolves = struct.unpack("B", self._sock.recv(1))[0]
            self._map[y_case, x_case] = [nb_humans, nb_vampires, nb_werewolves]

    def end_game(self):
        """ End the game and close the socket """
        self.is_running = False
        self._sock.close()

    def _load_set(self):
        """ Receive the SET information (shape of the map) """
        set_code = self._sock.recv(3).decode()
        assert set_code == "SET"
        n = struct.unpack("B", self._sock.recv(1))[0]
        m = struct.unpack("B", self._sock.recv(1))[0]
        self._shape = n, m

    def _load_humans(self):
        """ Receive the HUM information (location of the humans) """
        human_code = self._sock.recv(3).decode()
        assert human_code == "HUM"
        n_maison = struct.unpack("B", self._sock.recv(1))[0]
        list_coordonnees = []
        for _ in range(n_maison):
            x = struct.unpack("B", self._sock.recv(1))[0]
            y = struct.unpack("B", self._sock.recv(1))[0]
            list_coordonnees.append((x, y))
        self._houses = list_coordonnees

    def _load_home(self):
        """ Reçeive the HME information (start coordinates)"""
        home_code = self._sock.recv(3).decode()
        assert home_code == "HME"
        x_start = struct.unpack("B", self._sock.recv(1))[0]
        y_start = struct.unpack("B", self._sock.recv(1))[0]
        self._start = y_start, x_start

    def _load_map(self):
        """ Receive information concerning the starting map """
        map_code = self._sock.recv(3).decode()
        assert map_code == "MAP"
        n_map = struct.unpack("B", self._sock.recv(1))[0]
        self._map = np.zeros((*self._shape, 3))
        self._update_cells(n_map)

    def load_initial_parameters(self):
        """ Loads all the starting parameters """
        self._load_set()
        self._load_humans()
        self._load_home()
        self._load_map()
