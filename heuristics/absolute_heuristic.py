from numpy import ndarray
from lib.util import distance_nb_coups
from lib.positions import get_all_positions


def absolute_heuristic(map: ndarray, type:str):
    """
    This heuristic is trying to quantify the advantaging position
    of a team uppon an other
    """
    humans_positions, our_positions, opponent_positions = get_all_positions(map, type)
    w_us, w_adv, w_hum = 1, 1, 1
    score = 0
    
    # calculate our score regarding the current state of the map
    for us_position in our_positions.keys():
        # value_list = []
        nb_us = our_positions[us_position]
        # value = nb_us * w_us # use to rise the interest of eating ennemies
        value = 0
        for oppo_position in opponent_positions.keys():
            nb_oppo = opponent_positions[oppo_position]
            distance_us_oppo = distance_nb_coups(us_position, oppo_position)
            if nb_us >= 1.5*nb_oppo:
                value += w_adv / ( distance_us_oppo * (1.51 - nb_oppo/nb_us))
            else:
                if nb_us >= nb_oppo:
                    probability_of_win = nb_us / nb_oppo - 0.5
                else:
                    probability_of_win = nb_us / (2 * nb_oppo)
                value += probability_of_win*w_adv / distance_us_oppo

        for human_position in humans_positions.keys():
            nb_human = humans_positions[human_position]
            distance_us_human = distance_nb_coups(us_position, human_position)
            if nb_us>=nb_human:
                value += w_hum / (distance_us_human * (1.01 - nb_human/nb_us))
            else:
                probability_of_win = nb_us / (2 * nb_human)
                value += probability_of_win * w_hum / distance_us_human - 0.5
        score += value

    # calculate the opponent score regarding the current state of the map
    for oppo_position in opponent_positions.keys():
        nb_oppo = opponent_positions[oppo_position]
        # value = w_us * nb_oppo
        value = 0
        for us_position in our_positions.keys():
            nb_us = our_positions[us_position]
            distance_oppo_us = distance_nb_coups(oppo_position, us_position)
            if nb_oppo >= 1.5*nb_us:
                value += w_adv / (distance_oppo_us * (1.51 - nb_us/nb_oppo))
            else:
                if nb_oppo >= nb_us:
                    probability_of_win = nb_oppo / nb_us - 0.5
                else:
                    probability_of_win = nb_oppo / (2 * nb_us)
                value += probability_of_win*w_adv / distance_oppo_us
        for human_position in humans_positions.keys():
            nb_human = humans_positions[human_position]
            distance_oppo_human = distance_nb_coups(oppo_position, human_position)
            if nb_oppo>=nb_human:
                value += w_hum / (distance_oppo_human * (1.01 - nb_human/nb_oppo))
            else:
                probability_of_win = nb_oppo / (2 * nb_human)
                value += probability_of_win * w_hum / distance_us_human - 0.5
        score -= value
    return score
