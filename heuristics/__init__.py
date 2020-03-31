from .absolute_heuristic import absolute_heuristic
from .heuristic_2 import heuristic_2

HEURISTICS = {
    "absolute": absolute_heuristic,
    "heuristic2": lambda state, species_played: heuristic_2(
        state,
        species_played,
        population_weight=10,
        absolute_win_weight=1,
        human_win_weight=100,
        winning_weight=100000,
    ),
}
