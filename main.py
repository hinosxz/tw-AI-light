from models.game import Game
from models.player import Player
from heuristics.h1 import *
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--name', '-N', help="Name of the player", type=str, default='JPP')
parser.add_argument('--host', '-H', help="the host to use", type=str, default='127.0.0.1')
parser.add_argument('--port', '-P', help="the port to use", type=int, default=5555)
args = parser.parse_args()

if __name__ == "__main__":
    Game = Game(args.host, args.port)
    Player = Player(args.name, Game)
    print(Game._type)
    while True:
        Game.update_map()
        moves_dict = heuristic1(Player, Game)
        print(moves_dict)
        Player.move(moves_dict)
