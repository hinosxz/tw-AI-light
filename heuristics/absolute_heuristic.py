from models.game import Game

from lib.util import manhattan_dist


def absolute_heuristic(game: Game):
    w_adv, w_hum = 1, 1
    houses_dict = game.get_humans_positions()
    opponent_dict = game.get_opponent_positions()
    our_dict = game.get_our_positions()
    score = 0

    # calculate our score regarding the current state of the map
    for us_position in our_dict.keys():
        value = 0
        value_list = []
        nb_us = our_dict[us_position]
        for oppo_position in opponent_dict.keys():
            nb_oppo = opponent_dict[oppo_position]
            distance_us_oppo = manhattan_dist(us_position, oppo_position)
            value += w_adv / distance_us_oppo * (nb_us / nb_oppo - 3 / 2)
        for human_position in houses_dict.keys():
            nb_human = houses_dict[human_position]
            distance_us_human = manhattan_dist(us_position, human_position)
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
            value += w_adv / distance_oppo_us * (nb_oppo / nb_us - 3 / 2)
        for human_position in houses_dict.keys():
            nb_human = houses_dict[human_position]
            distance_oppo_human = manhattan_dist(oppo_position, human_position)
            value += w_hum / distance_oppo_human * (nb_oppo / nb_human - 1)
        score -= value
    return score
