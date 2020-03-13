from numpy import ndarray

from lib.positions import get_human_positions, get_opponent_positions, get_our_positions

from lib.util import manhattan_dist


def absolute_heuristic(state: ndarray, game_type: str):
    w_adv, w_hum = 1, 1
    houses_dict = get_human_positions(state)
    opponent_dict = get_opponent_positions(state, game_type)
    our_dict = get_our_positions(state, game_type)
    score = 0

    # calculate our score regarding the current state of the map
    for us_position in our_dict.keys():
        value = 0
        value_list = []
        nb_us = our_dict[us_position]
        for oppo_position in opponent_dict.keys():
            nb_oppo = opponent_dict[oppo_position]
            distance_us_oppo = manhattan_dist(us_position, oppo_position)
            # FIXME find better alternative to avoid division by zero
            if distance_us_oppo and nb_oppo:
                value += w_adv / distance_us_oppo * (nb_us / nb_oppo - 3 / 2)
        for human_position in houses_dict.keys():
            nb_human = houses_dict[human_position]
            distance_us_human = manhattan_dist(us_position, human_position)
            # FIXME find better alternative to avoid division by zero
            if distance_us_human and nb_human:
                value += w_hum / distance_us_human * (nb_us / nb_human - 1)
        value_list.append(value)
        all_neg = True
        for val in value_list:
            if val >= 0:
                all_neg = False
                break
            else:
                # TODO find the heuristics which include the random battle
                pass
        score += value

    # calculate the opponent score regarding the current state of the map
    for oppo_position in opponent_dict.keys():
        value = 0
        nb_oppo = opponent_dict[oppo_position]
        for us_position in our_dict.keys():
            nb_us = our_dict[us_position]
            distance_oppo_us = manhattan_dist(oppo_position, us_position)
            # FIXME find better alternative to avoid division by zero
            if distance_oppo_us and nb_us:
                value += w_adv / distance_oppo_us * (nb_oppo / nb_us - 3 / 2)
        for human_position in houses_dict.keys():
            nb_human = houses_dict[human_position]
            distance_oppo_human = manhattan_dist(oppo_position, human_position)
            # FIXME find better alternative to avoid division by zero
            if distance_oppo_human and nb_human:
                value += w_hum / distance_oppo_human * (nb_oppo / nb_human - 1)
        score -= value
    return score
