from typing import Dict, Tuple

from numpy import ndarray

from lib.constants import TYPE_TO_OPPONENT_POSITION_INDEX, TYPE_TO_POSITION_INDEX


def get_positions(map: ndarray, index: int):
    positions: Dict[Tuple[int, int], int] = {}
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell[index] != 0:
                positions[(i, j)] = cell[index]
    return positions


def get_human_positions(map: ndarray):
    return get_positions(map, 0)


def get_opponent_positions(map: ndarray, type: str):
    return get_positions(map, TYPE_TO_OPPONENT_POSITION_INDEX[type])


def get_our_positions(map: ndarray, type: str):
    return get_positions(map, TYPE_TO_POSITION_INDEX[type])

def get_all_positions(map: ndarray, type: str):
    human_position: Dict[Tuple[int, int], int] = {}
    our_positions: Dict[Tuple[int, int], int] = {}
    opponent_positions: Dict[Tuple[int, int], int] = {}
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell[0] != 0:
                human_position[(i,j)] = cell[0]
            elif cell[TYPE_TO_POSITION_INDEX[type]] != 0:
                our_positions[(i,j)] = cell[TYPE_TO_POSITION_INDEX[type]]
            elif cell[TYPE_TO_OPPONENT_POSITION_INDEX[type]] != 0:
                opponent_positions[(i,j)] = cell[TYPE_TO_OPPONENT_POSITION_INDEX[type]]
    return human_position, our_positions, opponent_positions

