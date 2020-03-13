from math import ceil
import itertools
from heuristics.heuristic1 import distance_nb_coups
from operator import itemgetter
from copy import copy

ennemy_positions = {(2, 3): 2, (4, 3): 2, (5, 7): 2}

human_positions = {(10, 3): 4}

our_positions = {(2, 8): 11}


def compute_groups(our_positions: dict, ennemy_positions: dict, human_positions: dict):
    our_size = 0

    for key, value in our_positions.items():
        our_size = [key, value]

    sizes = []
    possibilities = [[our_size]]

    for key, value in ennemy_positions.items():
        sizes.append([key, ceil(1.5 * value)])

    for key, value in human_positions.items():
        sizes.append([key, value])

    sizes = sorted(sizes, key=itemgetter(1))
    for i in range(len(sizes)):
        j = i
        buffer_size = copy(our_size)
        buffer_split = []
        # TODO Limit minimal split size in a smarter way
        while j < len(sizes) and (buffer_size[1] - sizes[j][1]) >= sizes[j][1]:

            buffer_size[1] = buffer_size[1] - sizes[j][1]
            buffer_split.append([find_closest(our_size[0], sizes[j][0]), sizes[j][1]])
            possibility = [copy(buffer_size)] + buffer_split
            possibilities += [possibility]
            j += 1

    output = []
    for possibility in possibilities:

        j = len(sizes) - 1
        while possibility[0][1] < sizes[j][1]:
            j -= 1
        possibility[0][0] = find_closest(possibility[0][0], sizes[j][0])

        if possibility not in output:
            output.append(possibility)
    return output


def find_closest(our_position, target_position):
    if our_position[0] == target_position[0] and our_position[1] > target_position[1]:
        x0, y0 = our_position[0], our_position[1] - 1

    elif our_position[0] == target_position[0] and our_position[1] < target_position[1]:
        x0, y0 = our_position[0], our_position[1] + 1

    elif our_position[1] == target_position[1] and our_position[0] > target_position[0]:
        x0, y0 = our_position[0] - 1, our_position[1]

    elif our_position[1] == target_position[1] and our_position[0] < target_position[0]:
        x0, y0 = our_position[0] + 1, our_position[1]

    elif our_position[0] > target_position[0] and our_position[1] > target_position[1]:
        x0, y0 = our_position[0] - 1, our_position[1] - 1

    elif our_position[0] > target_position[0] and our_position[1] < target_position[1]:
        x0, y0 = our_position[0] - 1, our_position[1] + 1

    elif our_position[0] < target_position[0] and our_position[1] > target_position[1]:
        x0, y0 = our_position[0] + 1, our_position[1] - 1

    elif our_position[0] < target_position[0] and our_position[1] < target_position[1]:
        x0, y0 = our_position[0] + 1, our_position[1] + 1

    return tuple((x0, y0))


output = compute_groups(our_positions, ennemy_positions, human_positions)
print("Returned : " + str(output))
print("Length : " + str(len(output)))
