from itertools import product
from numpy import inf as infinity, ndarray, array, copy
from typing import Iterable, Tuple, List

from heuristics.absolute_heuristic import absolute_heuristic
from lib.constants import TYPE_TO_POSITION_INDEX, TYPE_TO_OPPONENT_POSITION_INDEX
from lib.positions import get_positions


OPPONENTS = {"vampire": "wolf", "wolf": "vampire"}


def game_is_over(state: ndarray):
    vampires = get_positions(state, 1).keys()
    werewolves = get_positions(state, 2).keys()
    return len(vampires) == 0 or len(werewolves) == 0


def cutoff_test(state: ndarray, depth: int, max_depth: int):
    return depth > max_depth or game_is_over(state)


def evaluate(state: ndarray, game_type: str):
    return absolute_heuristic(state, game_type)


def get_neighbors(cell, shape):
    p, q = shape[0], shape[1]
    i, j = cell
    return [
        (x2, y2)
        for x2 in range(i - 1, i + 2)
        for y2 in range(j - 1, j + 2)
        if (
            -1 < i < p
            and -1 < j < q
            and (i != x2 or j != y2)
            and (0 <= x2 < p)
            and (0 <= y2 < q)
        )
    ] + [cell]


def get_moves(
    group_position: Tuple[int, int], size: int, neighbors: List[Tuple[int, int]]
):
    return [(*group_position, size, *to) for to in neighbors]


def get_successors(state: ndarray, species: int):
    groups = get_positions(state, species)

    possible_moves_per_group = [
        get_moves(group_position, size, get_neighbors(group_position, state.shape))
        for group_position, size in groups.items()
    ]
    possible_moves: List[Tuple[Tuple[int, int, int, int, int], ...]] = list(
        product(*possible_moves_per_group)
    )

    successors: List[ndarray] = []
    for moves in possible_moves:
        successor = copy(state)
        for x_origin, y_origin, size, x_target, y_target in moves:
            successor[x_origin, y_origin, species] -= size
            successor[x_target, y_target, species] += size
        successors.append(successor)

    return successors, possible_moves


def alphabeta_search(species_played: str, state: ndarray, d=4):
    """

    :param species_played: Current game
    :param state: State of the current game
    :param d: Maximum depth
    :return: An action
    """

    def max_value(s: ndarray, alpha: int, beta: int, depth: int):
        if cutoff_test(s, depth, d):
            return evaluate(s, species_played), s
        v = -infinity
        next_state = s
        moves = []
        successor_states, successor_move_options = get_successors(
            state, TYPE_TO_POSITION_INDEX[species_played]
        )
        for k in range(len(successor_move_options)):
            successor_state = successor_states[k]
            successor_moves = successor_move_options[k]
            next_min = min_value(successor_state, alpha, beta, depth + 1)[0]
            if next_min > v:
                v = next_min
                next_state = successor_state
                moves = successor_moves
            if v >= beta:
                return v, next_state, moves
            alpha = max(alpha, v)
        return v, next_state, moves

    def min_value(s: ndarray, alpha: int, beta: int, depth: int):
        if cutoff_test(s, depth, d):
            return evaluate(s, OPPONENTS[species_played]), s
        v = infinity
        next_state = s
        moves = []
        successor_states, successor_move_options = get_successors(
            state, TYPE_TO_OPPONENT_POSITION_INDEX[species_played]
        )
        for k in range(len(successor_move_options)):
            successor_state = successor_states[k]
            successor_moves = successor_move_options[k]
            next_max = max_value(successor_state, alpha, beta, depth + 1)[0]
            if next_max < v:
                v = next_max
                next_state = successor_state
                moves = successor_moves
            if v <= alpha:
                return v, next_state, moves
            beta = min(beta, v)
        return v, next_state, moves

    _value, _map, next_move_iterator = max_value(state, -infinity, infinity, 0)
    next_moves = []
    for x_origin, y_origin, size, x_target, y_target in next_move_iterator:
        next_moves.append(
            {
                "from_position": [x_origin, y_origin],
                "number": size,
                "to_position": [x_target, y_target],
            }
        )
    return next_moves


# Example state to test
# example = array([
#         [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 0, 0], [0, 0, 0]],
#         [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
#         [[0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
#         [[0, 0, 0], [0, 3, 0], [0, 0, 3], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
#         [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0]],
#     ])
# print(alphabeta_search("vampire", example))
