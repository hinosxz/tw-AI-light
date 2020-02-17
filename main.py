from command import Game
from client import Player
from h1 import *
import time

if __name__ == "__main__":
    Game = Game('192.168.56.1')
    Player = Player('barth', Game)
    print(Game._type)
    while True:
        Game.update_map()
        moves_dict = heuristic1(Player, Game)
        print(moves_dict)
        Player.move(moves_dict)
