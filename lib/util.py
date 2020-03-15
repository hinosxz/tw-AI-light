from typing import List, Tuple
from numpy import ndarray
import numpy as np
import itertools
from lib.constants import TYPE_TO_POSITION_INDEX


def manhattan_dist(d1, d2):
    return ((d1[0] - d2[0]) ** 2 + (d1[1] - d2[1]) ** 2) ** 0.5


def sign_integer(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def flatten(array: Tuple[List[Tuple[int, int, int, int, int]]]):
    """
    Flattens move tuple a single level deep
    """
    flat_list = []
    for sublist in array:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def distance_nb_coups(pos_1, pos_2):
    # We calculate the number of moves to do in diagonal
    x_init, y_init = pos_1
    x_final, y_final = pos_2
    nb_moves_diagonal = min(abs(x_init - x_final), abs(y_init - y_final))
    # We calculate the number of moves to do in line
    x_init -= nb_moves_diagonal * sign_integer(x_init - x_final)
    y_init -= nb_moves_diagonal * sign_integer(y_init - y_final)
    nb_moves_line = max(abs(x_init - x_final), abs(y_init - y_final))
    return nb_moves_diagonal + nb_moves_line

def from_map_to_moves(initial_map: ndarray, final_map: ndarray, type:str):
    moves_list = []
    intermediate_map = np.subtract(final_map.copy(),initial_map.copy())
    our_index = TYPE_TO_POSITION_INDEX[type]
    for i, row in enumerate(intermediate_map):
        for j, cell in enumerate(row):
            if cell[our_index] < 0:
                for k,l in itertools.product([-1,0,1],[-1,0,1]):
                    if (i+k>0
                    and i+k<initial_map.shape[0]
                    and j+l>0
                    and j+l<initial_map.shape[1]):
                        if final_map[i+k,j+l,our_index] > 0:
                            from_position = [i,j]
                            to_position = [i+k,j+l]
                            number = - cell[our_index]
                            moves_list.append({
                                            'from_position': from_position,
                                            'number': number,
                                            'to_position': to_position
                                            })
    return moves_list

