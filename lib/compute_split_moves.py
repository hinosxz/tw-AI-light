from typing import List, Tuple
from lib.util import get_neighbors, get_moves


def couple_size_split(size: int):
    split_couples: List[Tuple[int, int]] = []
    first_size: int = size - 1
    last_size: int = 1
    while first_size > 0:
        split_couples.append((first_size, last_size))
        first_size -= 1
        last_size += 1
    return split_couples


def compute_all_couple_targets(next_positions: List[Tuple[int, int]]):
    couple_targets: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    nb_pos = len(next_positions)
    for i in range(nb_pos):
        first_pos = next_positions[i]
        for j in range(i + 1, nb_pos):
            couple_targets.append((first_pos, next_positions[j]))
    return couple_targets


def compute_all_possible_moves_for_one_group(
    size: int, cell: Tuple[int, int], shape: Tuple[int, int]
):
    next_positions = get_neighbors(cell, shape, True)
    moves_without_split = [[move] for move in get_moves(cell, size, next_positions)]
    couple_targets = compute_all_couple_targets(next_positions)
    couple_sizes = couple_size_split(size)
    moves: List[List[Tuple[int, int, int, int, int]]] = moves_without_split
    for first_size, second_size in couple_sizes:
        for first_pos, second_pos in couple_targets:
            local_moves: List[Tuple[int, int, int, int, int]] = []
            if cell != first_pos:
                local_moves.append((*cell, first_size, *first_pos))
            if cell != second_pos:
                local_moves.append((*cell, second_size, *second_pos))
            moves.append(local_moves)
    return moves
