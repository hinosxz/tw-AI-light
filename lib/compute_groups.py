from copy import copy
from math import ceil
from operator import itemgetter
from numpy import inf as infinity
from typing import Dict, Tuple, List, Union

from lib.util import manhattan_dist


def compute_groups(
    our_positions: Dict[Tuple[int, int], int],
    enemy_positions: Dict[Tuple[int, int], int],
    human_positions: Dict[Tuple[int, int], int],
    max_groups: int,
):
    our_size = [(0, 0), 0]
    for key, value in our_positions.items():
        # We initialize our group position with current position. TODO : manage multiples groups
        our_size = [key, value]
    init_pos = our_size[0]
    sizes = []

    for key, value in enemy_positions.items():
        sizes.append((key, ceil(1.5 * value)))

    for key, value in human_positions.items():
        sizes.append((key, value))

    sizes = sorted(sizes, key=itemgetter(1))
    # We retrieve all possible target groups and sort them from smallest to biggest

    if max_groups == 1:
        # If we cannot split, we only find most useful direction for the main group to aim for
        # CURRENT MOST USEFUL DIRECTION : to the biggest killable group
        buffer = copy(our_size)
        buffer[0] = find_closest_target([our_size], sizes)
        possibilities = [[to_move_list(buffer, init_pos)]]
        return possibilities

    buffer = copy(our_size)
    buffer[0] = find_closest_target([our_size], sizes)
    possibilities = [[to_move_list(buffer, init_pos)]]

    for i in range(len(sizes)):
        j = i
        buffer_us = copy(buffer)
        buffer_split = []
        addresses = []
        while (
            j < len(sizes)
            and (buffer_us[1]) - sizes[j][1] >= sizes[j][1]
            and (len(buffer_split) + 1 < max_groups)
        ):
            # We loop over each element, computing each splits possible, and trying to split more as much as possible
            # No split criteria : if split group would be smaller than currently observed group. Maybe improvable ?
            buffer_us[1] -= sizes[j][1]
            new_pos = get_next_cell(init_pos, sizes[j][0])
            new_target_pos = find_closest_target([[init_pos, buffer_us[1]]], sizes)

            if new_pos not in addresses + [new_target_pos]:
                # Goal is to merge dupes, as only 8 destinations, if we move, are possible
                # So if computed new destination was never seen, we include it in a list and store the possibility
                addresses.append(new_pos)
                buffer_split.append(to_move_list([new_pos, sizes[j][1]], init_pos))
                buffer_us = copy(buffer_us)
                buffer_us[0] = new_target_pos
                possibility = [to_move_list(copy(buffer_us), init_pos)] + buffer_split
                possibilities += [possibility]

            else:
                if new_pos in addresses:  # actually never occurs
                    # Else, if we already saw the possibility, and that possibility is not the initial group, then we
                    # add its vale to concerned group
                    print("flag")
                    merge_with = [x for x, y in enumerate(addresses) if y == new_pos]
                    buffer_split[merge_with[0]][1] += sizes[j][1]
                    possibility = [copy(buffer_us)] + buffer_split
                    possibilities += [possibility]
            j += 1

    return possibilities


def get_next_cell(our_position, target_position):
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

    return x0, y0


def find_closest_target(
    possibility: List[Tuple[Tuple[int, int], int]],
    targets: List[Tuple[Tuple[int, int], int]],
):
    """
    :param possibility: List of our positions
    :param targets: List of target (opponent + human) positions
    :return: the next cell that moves us the closest to the closest target
    """

    # FIXME Only handles one group of our own for now

    min_dist = infinity
    closest_target = targets[0][0]
    our_pos, our_size = possibility[0]
    for target_pos, target_size in targets:
        dist = manhattan_dist(our_pos, target_pos)
        if dist < min_dist:
            min_dist = dist
            closest_target = target_pos

    return get_next_cell(our_pos, closest_target)


def to_move_list(move: Tuple[Tuple[int, int], int], pos: Tuple[int, int]):
    target_pos, target_size = move
    return [pos[0], pos[1], target_size, target_pos[0], target_pos[1]]


# enemy_positions = {(2, 13): 2, (4, 12): 2, (5, 7): 2}
# human_positions = {(10, 3): 4}
# our_positions = {(2, 8): 11}
#
# start = time()
# output = compute_groups(our_positions, enemy_positions, human_positions, 4)
# end = time()
#
# print("Returned : " + str(output))
# print("Length : " + str(len(output)))
# print(f"Time : {end - start}")
