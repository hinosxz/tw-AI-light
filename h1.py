from client import Player
from command import Game
import itertools
import time 

def manhattan_dist(d1,d2):
    return ((d1[0]-d2[0])**2+(d1[1]-d2[1])**2)**(0.5)

def heuristic1(Player, Game):
    moves_dict = {}
    w0,w1,w2 = (1,1,1)
    opponent_dict = Game.get_opponent_position()
    humans_dict = Game.get_humans_dict()
    for i,group in enumerate(Player.get_species().groups()):
        position_x, position_y = group.get_position()
        max_value = -100000
        max_move = (0,0)
        for move in itertools.product([-1,0,1],[-1,0,1]):
            value = 0
            if move[0]!=0 or move[1]!=0:
                group.move(position_x + move[0], position_y + move[1])
                d_0, n_0 = group.get_position(), group.get_size()
                for op_group in opponent_dict.keys():
                    n_1, d_1 = opponent_dict[op_group], op_group
                    dist_0_1 = manhattan_dist(d_0,d_1)
                    if dist_0_1 != 0:
                        for hu_group in humans_dict.keys():
                            n_2, d_2 = humans_dict[hu_group], hu_group
                            dist_0_2 = manhattan_dist(d_0,d_2)
                            if dist_0_2 != 0:
                                value += w0*n_0 + w1/manhattan_dist(d_0,d_1)*(n_0/n_1-3/2) + w2/manhattan_dist(d_0,d_2)*(n_0/n_2-1)
                            else:
                                if n_0 >= n_2:
                                    value += 10000000
                                else:
                                    value -= 10000000
                    else:
                        if n_0 >= 3/2*n_1:
                            value += 1000000
                        else:
                            value -= 1000000
                if value > max_value:
                    max_value = value
                    max_move = move
                group.move(position_x,position_y)
        time.sleep(1)
        moves_dict[i] = {'from_position':[position_x,position_y],'number':n_0,'to_position':[position_x + max_move[0],position_y + max_move[1]]}
    return moves_dict