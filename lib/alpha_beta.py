from numpy import inf as infinity, ndarray, array, copy, array_equal
from numpy.random import binomial
from typing import Tuple, List
from time import time
from treelib import Tree
from uuid import uuid4

from heuristics import HEURISTICS
from lib.constants import TYPE_TO_POSITION_INDEX, TYPE_TO_OPPONENT_POSITION_INDEX
from lib.positions import get_positions, get_our_size, get_opponent_size
from lib.TimeoutException import TimeoutException
from lib.compute_split_moves import compute_all_possible_moves

MAX_RESPONSE_TIME = 1.9
OPPONENTS = {"vampire": "wolf", "wolf": "vampire"}


def is_game_over(state: ndarray):
    vampires = get_positions(state, 1).keys()
    werewolves = get_positions(state, 2).keys()
    return len(vampires) == 0 or len(werewolves) == 0


def is_cutoff_state(state: ndarray, depth: int, max_depth: int):
    return depth >= max_depth or is_game_over(state)


def has_timed_out(start_time: float):
    delta_time = time() - start_time
    return delta_time > MAX_RESPONSE_TIME


def evaluate(state: ndarray, game_type: str, heuristic_played: str) -> float:
    """
    Evaluate a state given a certain heuristic
    :param state:
    :param game_type:
    :param heuristic_played:
    :return: An integer score
    """
    heuristic = HEURISTICS[heuristic_played]
    return heuristic(state, game_type)


def get_successors(state: ndarray, species_index: int):
    """
    Given a map and a species, it computes interesting moves to generate a list of successor states worth evaluating
    :param state:
    :param species_index:
    :return: The list of successor maps and related moves
    """
    groups = get_positions(state, species_index)

    possible_moves = compute_all_possible_moves(groups, state.shape)
    filtered_possible_moves = []
    successors: List[ndarray] = []
    for moves in possible_moves:
        successor = copy(state)
        for x_origin, y_origin, size, x_target, y_target in moves:
            successor[x_origin, y_origin, species_index] -= size
            successor[x_target, y_target, species_index] += size
            successor[x_target, y_target] = check_conflict(
                successor[x_target, y_target], species_index
            )
        if not array_equal(state, successor):
            successors.append(successor)
            filtered_possible_moves.append(moves)
    return successors, filtered_possible_moves


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
    species_played: str, state: ndarray, d=4, heuristic_played: str = "monogroup"
):
    """
    MiniMax algorithm with alpha-beta pruning
    :param heuristic_played: Choice of heuristic
    :param species_played: Current game
    :param state: State of the current game
    :param d: Maximum depth
    :return: The list of best moves to perform this turn
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
        if has_timed_out(start):
            raise TimeoutException(moves)
        if is_cutoff_state(s, depth, d):
            return evaluate(s, species_played, heuristic_played), s, moves
        v = -infinity
        next_state = s
        next_moves = moves
        successor_states, successor_move_options = get_successors(
            s, TYPE_TO_POSITION_INDEX[species_played]
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
        if has_timed_out(start):
            raise TimeoutException(moves)
        if is_cutoff_state(s, depth, d):
            return evaluate(s, species_played, heuristic_played), s, moves
        v = infinity
        next_state = s
        next_moves = moves
        successor_states, successor_move_options = get_successors(
            s, TYPE_TO_OPPONENT_POSITION_INDEX[species_played]
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
