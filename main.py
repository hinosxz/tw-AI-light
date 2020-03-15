from models.game import Game
from models.player import Player
from heuristics.heuristic1 import heuristic1
from lib.alpha_beta import alphabeta_search
from lib.util import from_map_to_moves
import argparse
import numpy as np


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
            current_map = game.get_map().astype(np.int16)
            new_state = alphabeta_search(player.type, game.get_map())
            moves_dict = from_map_to_moves(current_map, new_state[1].astype(np.int16), player.type)
            print(moves_dict)
            player.move(moves_dict)
