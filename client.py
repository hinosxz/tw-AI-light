import struct
from command import *

class Player:
    def __init__(self, name, Game):
        self._name = name
        self._species = None
        self._game = Game
        self._game.send_names(name)


    def assign_team(self, species):
        self._species = species

class Species:
    def __init__(self, type, total_nb, position_x, position_y):
        self._player = None
        self._type = type
        self._groups = [Group(type, self, total_nb, position_x, position_y)]
        self._total_nb = total_nb

    def groups(self):
        return self._groups

    def divise(self, group_1, nb1, nb2):
        group_1.change_size(nb1)
        self._groups.append(Group(type, self, nb2, position_x, position_y))

    def merge(self, group_1, group_2):
        self._groups.remove(group_1)
        self._groups.remove(group_2)
        self._groups.append(Group(type, self, group_1.get_size() + group_2.get_size(), group_1.get_position()))

class Group:
    def __init__(self, Species, size, position_x, position_y):
        self._species = Species 
        self._size = size
        self._position_x = position_x
        self._position_y = position_y

    def get_position(self):
        return self._position_x,self._position_y

    def get_size(self):
        return self._size

    def move(self, x, y):
        try:
            assert abs(x - self._position_x) <=1 and abs(y-self._position_y) <= 1
        except:
            raise ValueError('You moved the group too much')
        self._position_x = x
        self._position_y = y
    
    def change_size(self, value):
        self._size = value 