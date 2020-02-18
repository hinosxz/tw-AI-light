import struct
import socket
import numpy as np

class Game:
    """
    Cette classe sert à intéragir avec le serveur, où se déroule le jeu.

    Elle initie la connexion et update la map du terrain en fonction des messages qu'elle reçoit.

    Paramètres
    ----------
    sock : socket
        socket de connexion avec le serveur
    shape : list
        forme de la map
    houses : list of tuples
        localisation des maisons contenant les humains
    depart : list
        Coordonnées de départ
    map : numpy array
        Map du jeu (dimension shape x 3 - en 0 c'est le nombre d'humains, 1 le nombre de vampires et 2 le nombre de loups)
    type : string
        Type du joueur principal (vampire ou loup garous)
    is_running : boolean
        True si jeu est en cours False sinon
    """

    def __init__(self, hote="127.0.0.1", port=5555):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((hote, port))
        self._shape = None
        self._houses = None
        self._depart = None
        self._map = None
        self._type = None
        self.is_running = True

    def get_humans_positions(self):
        """
        Renvoie la position des humains sous forme de dictionnaires
        (x, y) : nb_humans
        avec (x, y) les coordonnées du groupe d'humains
        et nb_humans le nombre d'humains
        """
        humans_dict = {}
        for i, row in enumerate(self._map):
            for j, cell in enumerate(row):
                if cell[0] != 0:
                    humans_dict[(i,j)] = cell[0]
        print(humans_dict)
        return humans_dict

    def get_map(self):
        return self._map

    def get_opponent_positions(self):
        """
            Renvoie la position des opposants sous forme de dictionnaires
            (x, y) : nb_opponents
            avec (x, y) les coordonnées du groupe d'opposants
            et nb_opposants le nombre d'opposants
        """
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

    def get_start_info(self):
        """ 
        Renvoie les informations de départ
        
        - type des unités alliées (self._type - string)
        - nb d'unités alliées (total_nb - integer)
        - coordonnées de départ (self._depart - list)
        """
        start_cell = self._map[self._depart]
        total_nb = 0
        if start_cell[1] != 0:
            self._type = 'vampire'
            total_nb = start_cell[1]
        else:
            self._type = 'wolf'
            total_nb = start_cell[2]
        return self._type, total_nb, self._depart

    def send_name(self, name):
        """Envoie le nom du joueur au serveur"""
        msg_to_send = b'NME'
        msg_to_send += struct.pack("B", len(name))
        msg_to_send += name.encode()
        self._sock.send(msg_to_send)

    def send_move(self, moves_list):
        """Envoie une liste d'instructions au serveur"""
        msg_to_send = b'MOV'
        msg_to_send += struct.pack('B', len(moves_list))
        for move in moves_list:
            to_pos_x, to_pos_y = move['to_position']
            from_pos_x, from_pos_y = move['from_position']
            if type == 'vampire':
                self._map[to_pos_x, to_pos_y][1] = self._map[from_pos_x, from_pos_y][1] - move['number']
                self._map[from_pos_x, from_pos_y][1] -= move['number']
            if type == 'wolf':
                self._map[to_pos_x, to_pos_y][2] = self._map[from_pos_x, from_pos_y][2] - move['number']
                self._map[from_pos_x, from_pos_y][2] -= move['number']
            msg_to_send += struct.pack('B', int(move['from_position'][1]))
            msg_to_send += struct.pack('B', int(move['from_position'][0]))
            msg_to_send += struct.pack('B', int(move['number']))
            msg_to_send += struct.pack('B', int(move['to_position'][1]))
            msg_to_send += struct.pack('B', int(move['to_position'][0]))
        self._sock.send(msg_to_send)

    def update_map(self):
        """ Met à jour la map en fonction des informations reçues"""
        upd_code = self._sock.recv(3).decode()
        try:
            assert upd_code == 'UPD'
            nb_changes = struct.unpack('B', self._sock.recv(1))[0]
            self._update_cells(nb_changes)
        except AssertionError as e:
            end_message = self._sock.recv(3).decode()
            print(end_message)
            self.end_game()

    def _update_cells(self, nb_changes):
        """ Met à jour les cases en fonction des informations reçues """
        for i in range(nb_changes):
            x_case = struct.unpack('B', self._sock.recv(1))[0]
            y_case = struct.unpack('B', self._sock.recv(1))[0]
            nb_humans = struct.unpack('B', self._sock.recv(1))[0]
            nb_vampires = struct.unpack('B', self._sock.recv(1))[0]
            nb_werewolves = struct.unpack('B', self._sock.recv(1))[0]
            self._map[y_case, x_case] = [nb_humans, nb_vampires, nb_werewolves]

    def end_game(self):
        """ Termine le jeu et ferme la socket """
        self.is_running = False
        self._sock.close()

    def _load_set(self):
        """ Reçoit les informations concernant les dimensions du jeu """
        set_code = self._sock.recv(3).decode()
        assert set_code == 'SET'
        n = struct.unpack('B', self._sock.recv(1))[0]
        m = struct.unpack('B', self._sock.recv(1))[0]
        self._shape = n, m

    def _load_humans(self):
        """ Reçoit les informations concernant les humains du jeu """
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
        """ Reçoit les informations concernant les coordonnées de départ """
        home_code = self._sock.recv(3).decode()
        assert home_code == 'HME'
        x_depart = struct.unpack('B', self._sock.recv(1))[0]
        y_depart = struct.unpack('B', self._sock.recv(1))[0]
        self._depart = y_depart, x_depart

    def _load_map(self):
        """ Reçoit les informations concernant la map de départ """
        map_code = self._sock.recv(3).decode()
        assert map_code == 'MAP'
        n_map = struct.unpack('B', self._sock.recv(1))[0]
        self._map = np.zeros((*self._shape,3))
        self._update_cells(n_map)

    def _load_initial_parameters(self):
        """ Charge tous les paramètres de départ """
        # Getting the information about the map (SET)
        self._load_set()
        # Récupération des humains à setup sur la grille
        self._load_humans()
        # Case de départ
        self._load_home()
        # Get Map
        self._load_map()
