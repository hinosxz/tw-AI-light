from typing import Dict, Tuple

from numpy import ndarray

from lib.constants import TYPE_TO_OPPONENT_POSITION_INDEX, TYPE_TO_POSITION_INDEX


def get_positions(state: ndarray, index: int):
    positions: Dict[Tuple[int, int], int] = {}
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            if cell[index] != 0:
                positions[(i, j)] = cell[index]
    return positions


def get_human_positions(state: ndarray):
    return get_positions(state, 0)


def get_opponent_positions(state: ndarray, species_played: str):
    return get_positions(state, TYPE_TO_OPPONENT_POSITION_INDEX[species_played])


def get_our_positions(state: ndarray, species_played: str):
    return get_positions(state, TYPE_TO_POSITION_INDEX[species_played])


def get_our_size(state: ndarray, species_played: str):
    our_positions = get_our_positions(state, species_played)
    return sum(list(our_positions.values()))


def get_opponent_size(state: ndarray, species_played: str):
    their_positions = get_opponent_positions(state, species_played)
    return sum(list(their_positions.values()))
