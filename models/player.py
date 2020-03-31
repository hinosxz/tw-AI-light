from .specie import Specie


class Player:
    """
    This class represents a player of the game Vampires vs Werewolves.

    This is used to send the moves to the game and update local parameters

    Parameters
    ----------
    name : string
        name of the player
    game : Game
        Game to which the player is playing
    """

    def __init__(self, name, game):
        self._name = name
        self._species = None
        self._game = game
        self._game.send_name_to_server(name)
        self._game.load_initial_parameters()
        self.type, total_nb, depart = self._game.get_start_info()
        self._specie = Specie(self.type, total_nb, *depart)

    def move(self, moves_list):
        """
        This function take as an entry a list of dictionaries, containing each move to do.

        It updates the groups and then send the information to the Game object

        Parameters
        ----------
        moves_list : list of dictionaries
            {
                'from_position':
                'number':
                'to_position':
            }
        """
        for move in moves_list:
            try:
                group = self._specie.get_group(move["from_position"])
            except ValueError as exception:
                print(exception)
                continue

            if not (0 <= move["number"] <= 255):
                raise ValueError(
                    "// Value error: Group size must be between 0 and 255 - Group size = {}".format(
                        move["number"]
                    )
                )

            group.move(move["to_position"])
            group.increase_size(
                self._game.get_map()[move["to_position"][0], move["to_position"][1]][0]
            )

        self._game.send_move(moves_list)

    def get_species(self):
        return self._specie