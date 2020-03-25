from numpy import inf as infinity, ndarray, array, copy
from numpy.random import binomial
from typing import Tuple, List
from time import time
from treelib import Tree
from uuid import uuid4

from heuristics import HEURISTICS
from lib.constants import TYPE_TO_POSITION_INDEX, TYPE_TO_OPPONENT_POSITION_INDEX
from lib.compute_groups import compute_groups
from lib.positions import (
    get_positions,
    get_our_positions,
    get_opponent_positions,
    get_human_positions,
)
from lib.TimeoutException import TimeoutException

MAX_RESPONSE_TIME = 1.9
OPPONENTS = {"vampire": "wolf", "wolf": "vampire"}


def game_is_over(state: ndarray):
    vampires = get_positions(state, 1).keys()
    werewolves = get_positions(state, 2).keys()
    return len(vampires) == 0 or len(werewolves) == 0


def cutoff_test(state: ndarray, depth: int, max_depth: int):
    return depth >= max_depth or game_is_over(state)


def timeout_test(start_time: float):
    delta_time = time() - start_time
    return delta_time > MAX_RESPONSE_TIME


def evaluate(state: ndarray, game_type: str, heuristic_played: str):
    heuristic = HEURISTICS[heuristic_played]
    return heuristic(state, game_type)


def get_our_size(state: ndarray, species_played: str):
    our_positions = get_our_positions(state, species_played)
    return sum(list(our_positions.values()))


def get_opponent_size(state: ndarray, species_played: str):
    their_positions = get_opponent_positions(state, species_played)
    return sum(list(their_positions.values()))


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
    ]


def get_moves(
    group_position: Tuple[int, int], size: int, neighbors: List[Tuple[int, int]]
):
    return [(*group_position, size, *to) for to in neighbors]


def get_successors(state: ndarray, species: str, groups_limit: int):
    our_groups = get_our_positions(state, species)
    their_groups = get_opponent_positions(state, species)
    human_groups = get_human_positions(state)
    limit = groups_limit - len(our_groups)
    possible_moves = compute_groups(our_groups, their_groups, human_groups, limit)

    successors: List[ndarray] = []
    species_index = TYPE_TO_POSITION_INDEX[species]
    for moves in possible_moves:
        successor = copy(state)
        for x_origin, y_origin, size, x_target, y_target in moves:
            successor[x_origin, y_origin, species_index] -= size
            successor[x_target, y_target, species_index] += size
            successor[x_target, y_target] = check_conflict(
                successor[x_target, y_target], species_index
            )
        successors.append(successor)
    return successors, possible_moves


def check_conflict(current_cell: ndarray, player_index: int):
    """
    This function will make sure we don't engage in random battles and only simulate a potential win if we are
    actually able to win the fight for sure
    :param current_cell:
    :param player_index:
    :return: The cell after battle
    """
    cell = copy(current_cell)
    nb_humans = cell[0]
    nb_player = cell[player_index]
    opponent_index = (player_index % 2) + 1
    nb_opponent = cell[opponent_index]
    if nb_humans > 0 and nb_player > 0:
        if nb_player >= nb_humans:
            cell[0] = 0
            cell[player_index] += nb_humans
        else:
            probability_of_win = nb_player / (2 * nb_humans)
            cell[player_index] = 0
            cell[0] = binomial(nb_humans, 1 - probability_of_win)
    elif nb_opponent > 0 and nb_player > 0:
        if nb_player >= 1.5 * nb_opponent:
            cell[opponent_index] = 0
        else:
            if nb_player > nb_opponent:
                probability_of_win = nb_player / nb_opponent - 0.5
                cell[opponent_index] = 0
                cell[player_index] = round(probability_of_win * nb_player)
            else:
                probability_of_win = nb_player / (2 * nb_opponent)
                cell[player_index] = 0
                cell[opponent_index] = round((1 - probability_of_win) * nb_player)
    return cell


def alphabeta_search(
    species_played: str, state: ndarray, d=4, heuristic_played: str = "heuristic2", groups_limit=4
):
    """

    :param heuristic_played:
    :param species_played: Current game
    :param state: State of the current game
    :param d: Maximum depth
    :param groups_limit: Maximum number of groups allowed
    :return: An action
    """

    start_time = time()
    tree = Tree()

    def max_value(
        s: ndarray,
        moves: Tuple[Tuple[int, int, int, int, int], ...],
        alpha: int,
        beta: int,
        depth: int,
        start: float,
        t: Tree,
        parent: str,
    ):
        if timeout_test(start):
            raise TimeoutException(moves)
        if cutoff_test(s, depth, d):
            return evaluate(s, species_played, heuristic_played), s, moves
        v = -infinity
        next_state = s
        next_moves = moves
        successor_states, successor_move_options = get_successors(
            s, species_played, groups_limit
        )
        for k in range(len(successor_move_options)):
            successor_state = successor_states[k]
            successor_moves = successor_move_options[k]
            try:
                # For debugging purposes, add tree node with the computed score
                uid = str(uuid4())
                t.create_node(uid, uid, parent=parent)

                next_min = min_value(
                    successor_state,
                    successor_moves,
                    alpha,
                    beta,
                    depth + 1,
                    start,
                    t,
                    parent=uid,
                )[0]

                t.get_node(uid).tag = "{} - Us: {} vs Them: {}".format(
                    next_min,
                    get_our_size(successor_state, species_played),
                    get_opponent_size(successor_state, species_played),
                )
            except TimeoutException:
                raise TimeoutException(next_moves)

            if next_min > v:
                v = next_min
                next_state = successor_state
                next_moves = successor_moves
            if v >= beta:
                return v, next_state, next_moves
            alpha = max(alpha, v)
        return v, next_state, next_moves

    def min_value(
        s: ndarray,
        moves: Tuple[Tuple[int, int, int, int, int], ...],
        alpha: int,
        beta: int,
        depth: int,
        start: float,
        t: Tree,
        parent: str,
    ):
        if timeout_test(start):
            raise TimeoutException(moves)
        if cutoff_test(s, depth, d):
            return evaluate(s, species_played, heuristic_played), s, moves
        v = infinity
        next_state = s
        next_moves = moves
        successor_states, successor_move_options = get_successors(
            s, OPPONENTS[species_played], groups_limit
        )
        for k in range(len(successor_move_options)):
            successor_state = successor_states[k]
            successor_moves = successor_move_options[k]
            try:
                # For debugging purposes, add tree node with the computed score
                uid = str(uuid4())
                t.create_node(uid, uid, parent=parent)

                next_max = max_value(
                    successor_state,
                    successor_moves,
                    alpha,
                    beta,
                    depth + 1,
                    start,
                    t,
                    parent=uid,
                )[0]

                t.get_node(uid).tag = "{} - Us: {} vs Them: {}".format(
                    next_max,
                    get_our_size(successor_state, species_played),
                    get_opponent_size(successor_state, species_played),
                )
            except TimeoutException:
                raise TimeoutException(moves)

            if next_max < v:
                v = next_max
                next_state = successor_state
                next_moves = successor_moves
            if v <= alpha:
                return v, next_state, next_moves
            beta = min(beta, v)
        return v, next_state, next_moves

    chosen_moves = []

    tree.create_node("Root", "root")
    try:
        _value, _map, move_iterator = max_value(
            state, (), -infinity, infinity, 0, start_time, tree, parent="root"
        )
        # print(tree.show())
    except TimeoutException as exception:
        print("// Timeout exception raised: returned the best move known at the moment")
        move_iterator = exception.moves

    for x_origin, y_origin, size, x_target, y_target in move_iterator:
        chosen_moves.append(
            {
                "from_position": [x_origin, y_origin],
                "number": size,
                "to_position": [x_target, y_target],
            }
        )
    return chosen_moves


# Example state to test
example = array(
    [
        [[0, 0, 0], [7, 0, 0], [0, 0, 0]],
        [[0, 0, 8], [0, 0, 0], [0, 8, 0]],
        [[0, 0, 0], [7, 0, 0], [0, 0, 0]],
    ]
)

if __name__ == "__main__":
    print(alphabeta_search("vampire", example, d=4))
