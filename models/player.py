import struct
from .game import Game
from .species import Species
import time

class Player:
    def __init__(self, name, Game):
        self._name = name
        self._species = None
        self._game = Game
        self._game.send_name(name)
        self._game._load_initial_parameters()
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
