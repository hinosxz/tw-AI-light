def sign_integer(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


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



def absolute_heuristic(our_positions:dict, opponent_positions:dict, humans_positions:dict):
    """
    This heuristic is trying to quantify the advantaging position
    of a team uppon an other
    """

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
                value += w_adv / distance_us_oppo
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
                value += w_hum / distance_us_human
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
                value += w_adv / distance_oppo_us
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
                value += w_hum / distance_oppo_human
            else:
                probability_of_win = nb_oppo / (2 * nb_human)
                value += probability_of_win * w_hum / distance_us_human - 0.5
        score -= value
    return score
