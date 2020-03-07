import itertools
import time

from lib.util import manhattan_dist, sign_integer


def distance_nb_coups(pos_1, pos_2):
    # We calculate the number of moves to do in diagonal
    x_init, y_init = pos_1
    x_final, y_final = pos_2
    nb_moves_diagonal = min(abs(x_init - x_final), abs(y_init - y_final))
    # We calculate the number of moves to do in line
    x_init -= nb_moves_diagonal * sign_integer(x_init - x_final)
    y_init -= nb_moves_diagonal * sign_integer(y_init - y_final)
    nb_moves_line = max(abs(x_init - x_final), abs(y_init - y_final))
    return nb_moves_diagonal + nb_moves_line


def is_valid_position(x, y):
    return x >= 0 and y >= 0


def heuristic1(player, game):
    moves_list = []
    w0, w1, w2 = (1, 1, 1)
    opponent_dict = game.get_opponent_positions()
    humans_dict = game.get_human_positions()
    for i, group in enumerate(player.get_species().get_groups()):
        position_x, position_y = group.get_position()
        max_value = -100000
        max_move = (0, 0)
        for move in itertools.product([-1, 0, 1], [-1, 0, 1]):
            value = 0
            x, y = [position_x + move[0], position_y + move[1]]
            if is_valid_position(x, y) and (move[0] != 0 or move[1] != 0):
                group.move([x, y])
                d_0, n_0 = group.get_position(), group.get_size()
                for op_group in opponent_dict.keys():
                    n_1, d_1 = opponent_dict[op_group], op_group
                    dist_0_1 = manhattan_dist(d_0, d_1)
                    if dist_0_1 != 0:
                        for hu_group in humans_dict.keys():
                            n_2, d_2 = humans_dict[hu_group], hu_group
                            dist_0_2 = manhattan_dist(d_0, d_2)
                            if dist_0_2 != 0:
                                value += (
                                    w0 * n_0
                                    + w1
                                    / manhattan_dist(d_0, d_1)
                                    * (n_0 / n_1 - 3 / 2)
                                    + w2 / manhattan_dist(d_0, d_2) * (n_0 / n_2 - 1)
                                )
                            else:
                                if n_0 >= n_2:
                                    value += 10000000
                                else:
                                    value -= 10000000
                    else:
                        if n_0 >= 3 / 2 * n_1:
                            value += 1000000
                        else:
                            value -= 1000000
                if value > max_value:
                    max_value = value
                    max_move = move
                group.move([position_x, position_y])
        time.sleep(1)
        moves_list.append(
            {
                "from_position": [position_x, position_y],
                "number": n_0,
                "to_position": [position_x + max_move[0], position_y + max_move[1]],
            }
        )
    return moves_list
