from numpy import ndarray
from typing import Tuple, Dict

from lib.util import distance_nb_coups
from lib.positions import get_human_positions, get_our_positions, get_opponent_positions


def human_impact(
    our_positions: Dict[Tuple[int, int], int],
    humans_positions: Dict[Tuple[int, int], int],
    opponent_positions: Dict[Tuple[int, int], int],
    human_win_weight: int,
):
    human_impact_score = 0
    for human_position, human_size in humans_positions.items():
        for our_position, our_size in our_positions.items():
            distance = distance_nb_coups(our_position, human_position)
            if human_size <= our_size:
                human_impact_score += (
                    human_win_weight
                    * (our_size + human_size)
                    / ((distance ** 2) * our_size)
                )
        for opponent_position, opponent_size in opponent_positions.items():
            if human_size <= opponent_size:
                distance = distance_nb_coups(opponent_position, human_position)
                human_impact_score -= (
                    human_win_weight
                    * (opponent_size + human_size)
                    / ((distance ** 2) * opponent_size)
                )
    return human_win_weight


def population_impact(
    total_players: int,
    total_opponents: int,
    population_weight: int,
    winning_weight: int,
):
    if total_players == 0:
        return -winning_weight * total_opponents
    elif total_opponents == 0:
        return winning_weight * total_players
    else:
        return population_weight * (total_players - total_opponents)


def opponent_impact(
    our_positions: Dict[Tuple[int, int], int],
    opponent_positions: Dict[Tuple[int, int], int],
    absolute_win_weight: int,
    random_fight_weight: int,
):
    opponent_impact_score = 0
    for our_position, our_size in our_positions.items():
        for opponent_position, opponent_size in opponent_positions.items():
            distance = distance_nb_coups(our_position, opponent_position)
            if opponent_size >= 1.5 * our_size:
                opponent_impact_score -= absolute_win_weight * our_size / distance ** 2
            elif our_size >= 1.5 * opponent_size:
                opponent_impact_score += (
                    absolute_win_weight * opponent_size / distance ** 2
                )
            else:
                if our_size > opponent_size:
                    p = our_size / opponent_size - 0.5
                else:
                    p = our_size / (2 * opponent_size)
                opponent_impact_score += (
                    (opponent_size - our_size + 1) * (1 - p + p ** 2) / distance ** 2
                )

    return opponent_impact_score


def heuristic_2(
    state: ndarray,
    species_played: str,
    population_weight: float,
    absolute_win_weight: float,
    random_fight_weight: float,
    human_win_weight: float,
    winning_weight: float,
):
    humans_positions, our_positions, opponent_positions = (
        get_human_positions(state),
        get_our_positions(state, species_played),
        get_opponent_positions(state, species_played),
    )
    total_players = sum(list(our_positions.values()))
    total_opponents = sum(list(opponent_positions.values()))
    map_score = (
        population_impact(
            total_players, total_opponents, population_weight, winning_weight
        )
        + opponent_impact(
            our_positions, opponent_positions, absolute_win_weight, random_fight_weight
        )
        + human_impact(
            our_positions, humans_positions, opponent_positions, human_win_weight
        )
    )
    return map_score


if __name__ == "__main__":
    from lib.alpha_beta import example

    score = heuristic_2(
        state=example,
        species_played="vampire",
        population_weight=1000000,
        absolute_win_weight=1000,
        random_fight_weight=1000,
        human_win_weight=1000,
        winning_weight=1000000000,
    )

    print(score)
