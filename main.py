from models.Game import Game
from lib.alpha_beta import alphabeta_search
from argparse import ArgumentParser
from time import sleep
from heuristics import HEURISTICS

parser = ArgumentParser()
parser.add_argument(
    "--name", "-N", help="Name of the player", type=str, default="Group 3"
)
parser.add_argument(
    "--host", "-H", help="IP address of your game server", type=str, default="127.0.0.1"
)
parser.add_argument(
    "--port", "-P", help="Server port to connect to", type=int, default=5555
)
parser.add_argument(
    "--heuristic", help="Which heuristic to use", type=str, default="monogroup"
)
args = parser.parse_args()

if __name__ == "__main__":
    try:
        assert args.heuristic in HEURISTICS

        game = Game(args.host, args.port, args.name)
        print("// You are playing {}".format(game.type))
        turn = 0
        while game.is_running:
            game.update_map()
            sleep(1)
            if game.is_running:
                turn += 1
                moves = alphabeta_search(
                    game.type, game.get_map(), d=4, heuristic_played=args.heuristic
                )

                try:
                    game.send_move(moves)
                except ValueError as exception:
                    game.send_move([])
                    print(exception)

    except AssertionError:
        print(
            "// This heuristic is not available, please make sure you spelled its name correctly or use the default "
            "heuristic "
        )
