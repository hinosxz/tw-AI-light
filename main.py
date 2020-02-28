from models.game import Game
from models.player import Player
from heuristics.h1 import *
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--name", "-N", help="Name of the player", type=str, default="JPP2")
parser.add_argument(
    "--host", "-H", help="the host to use", type=str, default="127.0.0.1"
)
parser.add_argument("--port", "-P", help="the port to use", type=int, default=5555)
args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.host, args.port)
    player = Player(args.name, game)
    print("You are the {}".format(player.type))
    while game.is_running:
        game.update_map()
        if game.is_running:
            moves_dict = heuristic1(player, game)
            player.move(moves_dict)
