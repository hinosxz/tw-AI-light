from typing import Tuple


def sign_integer(value: int):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def distance_nb_moves(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    # We calculate the number of moves to do in diagonal
    x_init, y_init = pos_1
    x_final, y_final = pos_2
    nb_moves_diagonal = min(abs(x_init - x_final), abs(y_init - y_final))
    # We calculate the number of moves to do in line
    x_init -= nb_moves_diagonal * sign_integer(x_init - x_final)
    y_init -= nb_moves_diagonal * sign_integer(y_init - y_final)
    nb_moves_line = max(abs(x_init - x_final), abs(y_init - y_final))
    return nb_moves_diagonal + nb_moves_line
