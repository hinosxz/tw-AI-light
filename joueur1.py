import socket
import struct
import time

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect(('127.0.0.1', 5555))

msg_a_envoyer=b'NME'
msg_a_envoyer+= struct.pack('B', 7)
msg_a_envoyer+= b'Chuchu2'
print(msg_a_envoyer)
connexion_avec_serveur.send(msg_a_envoyer)

# Getting the information about the map (SET)
print(connexion_avec_serveur.recv(3).decode())
n = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
m = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
print("n: ", n)
print("m: ", m)

# Récupération des maisons à setup sur la grille
print(connexion_avec_serveur.recv(3).decode())
n_maison = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
print('n_maison:', n_maison)
list_coordonnees = []
for _ in range(n_maison):
    x = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    y = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    list_coordonnees.append((x, y))
print(list_coordonnees)

# Case de départ
print(connexion_avec_serveur.recv(3).decode())
x_depart = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
y_depart = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
print(x_depart, y_depart)

# MAP : Information de la Map
print(connexion_avec_serveur.recv(3).decode())
n_map = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
for _ in range(n_map):
    x_case = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    y_case = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    nb_humains = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    nb_vampires = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    nb_loup_garous = struct.unpack('B', connexion_avec_serveur.recv(1))[0]
    print("Sur la case {}, il y a {} humain(s), {} vampire(s) et {} loups garous".format((x_case, y_case), nb_humains, nb_vampires, nb_loup_garous))

pos_x = 5
pos_y = 4
nb_vampires_moved = 3

while True:
    # Wait for UPD information
    update_map = connexion_avec_serveur.recv(1024)
    print(update_map)
    print(update_map[:3].decode())
    if len(update_map) > 3:
        nb_changes = update_map[3]
        print(nb_changes)
        for i in range(nb_changes):
            start = 4 + i*5
            x_case = update_map[start]
            y_case = update_map[start+1]
            nb_humains = update_map[start+2]
            nb_vampires = update_map[start+3]
            nb_loup_garous = update_map[start+4]
            print("Sur la case {}, il y a {} humain(s), {} vampire(s) et {} loups garous".format((x_case, y_case), nb_humains, nb_vampires, nb_loup_garous))
    # Send Move
    time.sleep(2)
    move = b'MOV'
    nb_move = struct.pack('b', 1)
    start_coordinate = struct.pack('bb', pos_x, pos_y)
    if pos_x == 4:
        nb_vampires_moved = 4
    elif pos_x == 2:
        nb_vampires_moved = 5
    nb_people = struct.pack('b', nb_vampires_moved)
    if pos_x > 3:
        pos_x -= 1
    elif pos_x == 3 and pos_y > 2:
        pos_y -= 1
    elif pos_y == 2 and pos_x == 3:
        pos_x -= 1
    elif pos_y == 2 and pos_x == 2:
        pos_y += 1
    end_coordinate = struct.pack('bb', pos_x, pos_y)
    connexion_avec_serveur.send(move + nb_move + start_coordinate + nb_people + end_coordinate)
