from game import Game
from player import Player
from h1 import *
import time

if __name__ == "__main__":
    Game = Game('127.0.0.1')
    Player = Player('barth', Game)
    print(Game._type)
    while True:
        Game.update_map()
        moves_dict = heuristic1(Player, Game)
        print(moves_dict)
        Player.move(moves_dict)
