import struct
from command import *
import time

class Player:
    def __init__(self, name, Game):
        self._name = name
        self._species = None
        self._game = Game
        self._game.send_names(name)
        # time.sleep(1)
        print(self._game.get_map())
        if self._game.get_map() is not None:
            # assign the species to the player
            depart = self._game.get_depart()
            if self._game.get_map()[depart][1] != 0:
                total_nb = self._game.get_map()[depart][1]
                self._species = Species('vampire', total_nb, *depart)
                self._game.assign_type('vampire')
            elif self._game.get_map()[depart][2] != 0:
                total_nb = self._game.get_map()[depart][2]
                self._species = Species('wolf', total_nb, *depart)
                self._game.assign_type('wolf')
    
    # all the moves we want to make are saved in a dict,
    # the keys are the numero  of the move, it has the keys 
    # from_position, number and to_position
    def move(self, moves_dict):
        for key in moves_dict.keys():
            group = self._species.get_group(*moves_dict[key]['from_position'])
            if group.get_size() == moves_dict[key]['number']:
                group.move(*moves_dict[key]['to_position'])
                group.increase_size(self._game.get_map()[moves_dict[key]['to_position'][0],moves_dict[key]['to_position'][1]][0])
            elif group.get_size() > moves_dict[key]['number']:
                pass
            else:
                raise ValueError('You cannot move {} {}, the group on ({}) has a size of {}'.format(moves_dict[key]['number'], self._type, moves_dict[key]['from_position'], group.get_size()))
        self._game.send_move(moves_dict, self._species.get_type())

    def get_species(self):
        return self._species


class Species:

    def __init__(self, type, total_nb, position_x, position_y):
        self._type = type
        self._groups = [Group(total_nb, position_x, position_y)]
        self._total_nb = total_nb

    def get_type(self):
        return self._type

    def get_groups(self):
        return self._groups

    def get_group(self, x, y):
        for group in self.get_groups():
            if group.get_position() == [x,y]:
                return group
        raise ValueError('No group is on the position ({},{})'.format(x,y))

    # def divise(self, group_1, nb1, nb2):
    #     group_1.change_size(nb1)
    #     self._groups.append(Group(nb2, group_1.get_position()[0], group_1.get_position()[1]))

    # def merge(self, group_1, group_2):
    #     self._groups.remove(group_1)
    #     self._groups.remove(group_2)
    #     self._groups.append(Group(group_1.get_size() + group_2.get_size(), group_1.get_position()[0], group_1.get_position()[1]))

class Group:
    def __init__(self, size, position_x, position_y):
        self._size = size
        self._position_x = position_x
        self._position_y = position_y

    def get_position(self):
        return [self._position_x,self._position_y]

    def get_size(self):
        return self._size

    def move(self, x, y):
        try:
            assert abs(x - self._position_x) <=1 and abs(y-self._position_y) <= 1
        except:
            raise ValueError('You moved the group too much')
        self._position_x = x
        self._position_y = y
    
    def increase_size(self, amount):
        self._size += amount 