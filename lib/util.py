from typing import List, Tuple


def manhattan_dist(d1, d2):
    return ((d1[0] - d2[0]) ** 2 + (d1[1] - d2[1]) ** 2) ** 0.5


def sign_integer(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def flatten(array: Tuple[List[Tuple[int, int, int, int, int]]]):
    """
    Flattens move tuple a single level deep
    """
    flat_list = []
    for sublist in array:
        for item in sublist:
            flat_list.append(item)
    return flat_list
