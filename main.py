from models.game import Game
from lib.alpha_beta import alphabeta_search
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--name", "-N", help="Name of the player", type=str, default="JPP2")
parser.add_argument(
    "--host", "-H", help="the host to use", type=str, default="127.0.0.1"
)
parser.add_argument("--port", "-P", help="the port to use", type=int, default=5555)
args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args.host, args.port, args.name)
    print("You're playing {}".format(game.type))
    turn = 0
    while game.is_running:
        game.update_map()
        if game.is_running:
            turn += 1
            moves = alphabeta_search(game.type, game.get_map(), d=4)
            print("Turn #{}, moves : {}".format(turn, moves))
            try:
                game.send_move(moves)
            except ValueError as exception:
                game.send_move([])
                print(exception)
