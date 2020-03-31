from numpy import ndarray
from typing import Tuple, Dict

from lib.util import distance_nb_moves
from lib.positions import get_human_positions, get_our_positions, get_opponent_positions
from lib.constants import (
    WINNING_WEIGHT,
    ABSOLUTE_WIN_WEIGHT,
    POPULATION_WEIGHT,
    HUMAN_WIN_WEIGHT,
)


def compute_human_impact(
    our_size: int,
    human_size: int,
    our_position: Tuple[int, int],
    human_position: Tuple[int, int],
):
    local_human_score = 0
    distance = distance_nb_moves(our_position, human_position)
    if human_size <= our_size:
        local_human_score += (HUMAN_WIN_WEIGHT * human_size / distance) ** 2
    return local_human_score


def human_impact(
    our_positions: Dict[Tuple[int, int], int],
    humans_positions: Dict[Tuple[int, int], int],
    opponent_positions: Dict[Tuple[int, int], int],
):
    human_impact_score = 0
    for human_position, human_size in humans_positions.items():
        for our_position, our_size in our_positions.items():
            human_impact_score += compute_human_impact(
                our_size, human_size, our_position, human_position
            )

        # for opponent_position, opponent_size in opponent_positions.items():
        #    human_impact_score -= compute_human_impact(opponent_size, human_size, opponent_position, human_position)
    return human_impact_score


def population_impact(total_players: int, total_opponents: int):
    if total_players == 0:
        return -WINNING_WEIGHT * total_opponents
    elif total_opponents == 0:
        return WINNING_WEIGHT * total_players
    else:
        return POPULATION_WEIGHT * (total_players - total_opponents)


def compute_opponent_impact(
    our_size: int,
    opponent_size: int,
    our_position: Tuple[int, int],
    opponent_position: Tuple[int, int],
):
    distance = distance_nb_moves(our_position, opponent_position)
    if our_size >= 1.5 * opponent_size:
        local_opponent_score = (ABSOLUTE_WIN_WEIGHT * our_size / distance) ** 2
    elif opponent_size >= 1.5 * our_size:
        local_opponent_score = -(ABSOLUTE_WIN_WEIGHT * opponent_size / distance) ** 2
    elif our_size > opponent_size:
        local_opponent_score = ABSOLUTE_WIN_WEIGHT * opponent_size / (distance ** 2)
    else:
        local_opponent_score = -ABSOLUTE_WIN_WEIGHT * our_size / (distance ** 2)
    return local_opponent_score


def opponent_impact(
    our_positions: Dict[Tuple[int, int], int],
    opponent_positions: Dict[Tuple[int, int], int],
):
    opponent_impact_score = 0
    for our_position, our_size in our_positions.items():
        for opponent_position, opponent_size in opponent_positions.items():
            opponent_impact_score += compute_opponent_impact(
                our_size, opponent_size, our_position, opponent_position
            )
    return opponent_impact_score


def heuristic_2(state: ndarray, species_played: str):
    humans_positions, our_positions, opponent_positions = (
        get_human_positions(state),
        get_our_positions(state, species_played),
        get_opponent_positions(state, species_played),
    )
    total_players = sum(list(our_positions.values()))
    total_opponents = sum(list(opponent_positions.values()))
    map_score = (
        population_impact(total_players, total_opponents)
        + opponent_impact(our_positions, opponent_positions)
        + human_impact(our_positions, humans_positions, opponent_positions)
    )
    return map_score


if __name__ == "__main__":
    from lib.alpha_beta import example

    # For testing purposes
    score = heuristic_2(state=example, species_played="vampire")
    print(score)
