from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack

from numpy import zeros, uint8
from typing import Tuple, List

from lib.constants import TYPE_TO_POSITION_INDEX
from lib.positions import get_opponent_positions, get_our_positions


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
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.connect((host, port))
        self._shape = (0, 0)
        # Locations of humans
        self._houses: List[Tuple[int, int]] = []
        self._start = (0, 0)
        # _map[x, y] = [nb_humans, nb_vampires, nb_werewolves]
        self._map = zeros(0)
        self.type = ""
        self.is_running = True

    def get_map(self):
        return self._map

    def get_start_info(self):
        start_cell: List[int] = self._map[self._start]
        total_nb = start_cell[TYPE_TO_POSITION_INDEX[self.type]]
        return self.type, total_nb, self._start

    def is_over(self):
        return len(get_opponent_positions(self._map, self.type).keys()) == 0 or len(
            get_our_positions(self._map, self.type).keys()
        )

    def send_name_to_server(self, name):
        msg_to_send = b"NME"
        msg_to_send += pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)

    def send_move(self, moves_list):
        msg_to_send = b"MOV"
        msg_to_send += pack("B", len(moves_list))
        for move in moves_list:
            to_pos_x, to_pos_y = move["to_position"]
            from_pos_x, from_pos_y = move["from_position"]

            # Update the map
            self._map[to_pos_x, to_pos_y][TYPE_TO_POSITION_INDEX[self.type]] = (
                self._map[from_pos_x, from_pos_y][TYPE_TO_POSITION_INDEX[self.type]]
                - move["number"]
            )
            self._map[from_pos_x, from_pos_y][
                TYPE_TO_POSITION_INDEX[self.type]
            ] -= move["number"]

            msg_to_send += pack("B", int(move["from_position"][1]))
            msg_to_send += pack("B", int(move["from_position"][0]))
            msg_to_send += pack("B", int(move["number"]))
            msg_to_send += pack("B", int(move["to_position"][1]))
            msg_to_send += pack("B", int(move["to_position"][0]))
        self._sock.send(msg_to_send)

    def update_map(self):
        update_code = self._sock.recv(3).decode()
        try:
            assert update_code == "UPD"
            nb_changes: int = unpack("B", self._sock.recv(1))[0]
            self._update_cells(nb_changes)
        except AssertionError as e:
            self.end_game()

    def _update_cells(self, nb_changes: int, is_init=False):
        for _ in range(nb_changes):
            x: int = unpack("B", self._sock.recv(1))[0]
            y: int = unpack("B", self._sock.recv(1))[0]
            nb_humans: int = unpack("B", self._sock.recv(1))[0]
            nb_vampires: int = unpack("B", self._sock.recv(1))[0]
            nb_werewolves: int = unpack("B", self._sock.recv(1))[0]

            if is_init:
                y_start, x_start = self._start
                if x_start == x and y_start == y:
                    if nb_vampires != 0:
                        self.type = "vampire"
                    elif nb_werewolves != 0:
                        self.type = "wolf"
                    else:
                        raise IOError(
                            "Cannot initialize the game: there must be at least 1 vampire/wolf in the start cell"
                        )

            self._map[y, x] = [nb_humans, nb_vampires, nb_werewolves]

    def end_game(self):
        """ End the game and close the socket """
        self.is_running = False
        self._sock.close()

    def _load_set(self):
        """ Receive the SET information (shape of the map) """
        set_code = self._sock.recv(3).decode()
        assert set_code == "SET"
        n: int = unpack("B", self._sock.recv(1))[0]
        m: int = unpack("B", self._sock.recv(1))[0]
        self._shape = n, m

    def _load_humans(self):
        """ Receive the HUM information (location of the humans) """
        human_code = self._sock.recv(3).decode()
        assert human_code == "HUM"
        nb_houses = unpack("B", self._sock.recv(1))[0]
        list_coordinates: List[Tuple[int, int]] = []
        for _ in range(nb_houses):
            x: int = unpack("B", self._sock.recv(1))[0]
            y: int = unpack("B", self._sock.recv(1))[0]
            list_coordinates.append((x, y))
        self._houses = list_coordinates

    def _load_home(self):
        """ Receive the HME information (start coordinates)"""
        home_code = self._sock.recv(3).decode()
        assert home_code == "HME"
        x_start: int = unpack("B", self._sock.recv(1))[0]
        y_start: int = unpack("B", self._sock.recv(1))[0]
        self._start = y_start, x_start

    def _load_map(self):
        """ Receive information concerning the starting map """
        map_code = self._sock.recv(3).decode()
        assert map_code == "MAP"
        nb_changes: int = unpack("B", self._sock.recv(1))[0]
        self._map = zeros((*self._shape, 3), dtype=uint8)
        self._update_cells(nb_changes, is_init=True)

    def load_initial_parameters(self):
        """ Loads all the starting parameters """
        self._load_set()
        self._load_humans()
        self._load_home()
        self._load_map()
