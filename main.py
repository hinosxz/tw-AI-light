from command import Game
from client import Player
from h1 import *
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', help="Name of the player", type=str, required=True, default='JPP')
parser.add_argument('--host', '-h', help="the host to use", type=str, required=True, default='127.0.0.1')
parser.add_argument('--port', '-p', help="the port to use", type=str, required=True, default='5555')
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
