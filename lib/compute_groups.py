from math import ceil
from operator import itemgetter
from copy import copy

ennemy_positions = {(2, 3): 2, (4, 12): 2, (5, 7): 2}

human_positions = {(10, 3): 4}

our_positions = {(2, 8): 11}


def compute_groups(our_positions: dict, ennemy_positions: dict, human_positions: dict):
    our_size = 0

    for key, value in our_positions.items():
        our_size = [key, value]
    init_pos = our_size[0]
    sizes = []

    for key, value in ennemy_positions.items():
        sizes.append([key, ceil(1.5 * value)])

    for key, value in human_positions.items():
        sizes.append([key, value])

    sizes = sorted(sizes, key=itemgetter(1))

    buffer = copy(our_size)
    buffer[0] = find_closest_target([our_size], sizes)
    possibilities = [[buffer]]

    for i in range(len(sizes)):
        j = i
        buffer_us = copy(buffer)
        buffer_split = []
        addresses = []
        # TODO Limit minimal split size in a smarter way
        while j < len(sizes) and (buffer_us[1] - sizes[j][1]) >= sizes[j][1]:

            buffer_us[1] = buffer_us[1] - sizes[j][1]

            new_pos = find_closest(init_pos, sizes[j][0])

            new_target_pos = find_closest_target([[init_pos, buffer_us[1]]], sizes)

            print(new_pos)

            if new_pos not in addresses + [new_target_pos]:
                pos = copy(new_pos)
                addresses.append(pos)
                buffer_split.append([pos, sizes[j][1]])
                buffer_us = copy(buffer_us)
                buffer_us[0] = new_target_pos
                possibility = [copy(buffer_us)] + buffer_split
                possibilities += [possibility]

            else:
                if new_pos in addresses:
                    merge_with = [x for x, y in enumerate(addresses) if y == new_pos]
                    buffer_split[merge_with[0]][1] += sizes[j][1]
                    possibility = [copy(buffer_us)] + buffer_split
                    possibilities += [possibility]
            j += 1

    return possibilities


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


def find_closest_target(possibility, sizes):
    j = len(sizes) - 1
    while possibility[0][1] < sizes[j][1]:
        j -= 1
    return find_closest(possibility[0][0], sizes[j][0])


output = compute_groups(our_positions, ennemy_positions, human_positions)
print("Returned : " + str(output))
print("Length : " + str(len(output)))
