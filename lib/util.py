from typing import Tuple, List


def sign_integer(value: int):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def distance_nb_moves(pos_1: Tuple[int, int], pos_2: Tuple[int, int]):
    """
    :param pos_1:
    :param pos_2:
    :return: The number of moves to move from pos_1 to pos_2
    """
    # We calculate the number of moves to do in diagonal
    x_init, y_init = pos_1
    x_final, y_final = pos_2
    nb_moves_diagonal = min(abs(x_init - x_final), abs(y_init - y_final))
    # We calculate the number of moves to do in line
    x_init -= nb_moves_diagonal * sign_integer(x_init - x_final)
    y_init -= nb_moves_diagonal * sign_integer(y_init - y_final)
    nb_moves_line = max(abs(x_init - x_final), abs(y_init - y_final))
    return nb_moves_diagonal + nb_moves_line


def get_neighbors(
    cell: Tuple[int, int],
    shape: Tuple[int, int, int],
    with_start_position: bool = False,
):
    """
    :param cell:
    :param shape:
    :param with_start_position
    :return: The neighbor cells of the given cell, respecting the map shape
    """
    p, q = shape[0], shape[1]
    i, j = cell
    neighbors = [
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
    if with_start_position:
        neighbors.append((i, j))
    return neighbors


def get_moves(
    group_position: Tuple[int, int], size: int, neighbors: List[Tuple[int, int]]
):
    """
    :param group_position:
    :param size:
    :param neighbors:
    :return: A list of move tuples from group_position to each neighbor
    """
    return [(*group_position, size, *to) for to in neighbors]
