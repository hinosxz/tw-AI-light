import socket
from client import *


def load_static(L):
    # shape
    L = L[3:]
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
    return L, shape, houses_dict, depart

def load_map(L,shape):
    L = L[3:]
    nb_element = L.pop(0)
    M = np.zeros((shape[1],shape[0],3))
    for i in range(0,len(L),5):
        M[L[i],L[i+1]] = L[i+2:i+5]
    return nb_element,M

if __name__ == "__main__":

    hote = "192.168.56.1"
    port = 5555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    Player = Player('barth')
    NME(sock, Player)
    msg_recu = list(sock.recv(1024))
    print(msg_recu)

    first_map, shape, houses_dict, depart = load_static(msg_recu)
    if str([ord(x) for x in 'MAP'])[1:-1] in str(msg_recu):
        nb_element, first_map = load_map(first_map,shape)
        Wolf = Species('w', first_map(depart)[0], depart)
        Player.assign_species(Wolf)

    while True:
        new_msg = list(sock.recv(1024))
        if new_msg:
            if str([ord(x) for x in 'UPD'])[1:-1] in str(new_msg):
                print('yes')
                # do something




