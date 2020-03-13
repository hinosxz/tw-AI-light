ennemy_positions = {"a": 2, "b": 2, "c": 2}

human_positions = {"a": 4}

our_positions = {"a": 10}


def compute_groups(our_positions: dict, ennemy_positions: dict, human_positions: dict):

    our_size = 0

    for value in our_positions.values():
        our_size = value

    sizes = []
    possibilities = [[our_size]]

    for value in ennemy_positions.values():
        sizes.append(1.5 * value)

    for value in human_positions.values():
        sizes.append(value)

    sizes = sorted(sizes)
    print(sizes)
    for i in range(len(sizes)):
        print("Indices for " + str(i))
        j = i
        buffer_size = our_size
        buffer_split = []

        while j < len(sizes) and (buffer_size - sizes[j]) >= sizes[0]:
            print("Indices while " + str(j))
            buffer_size = buffer_size - sizes[j]
            buffer_split.append(sizes[j])
            print(
                "Buffer size " + str(buffer_size) + " Buffer split" + str(buffer_split)
            )
            possibility = [buffer_size] + buffer_split
            print(possibility)
            possibilities += [possibility]
            j += 1

    return set(tuple(i) for i in possibilities)
