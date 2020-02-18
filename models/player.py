import struct
from .game import Game
from .species import Species
import time

class Player:
    """
    Classe représentant un joueur du jeu Vampires vs Werewolves

    Cette classe sert à représenter un joueur, envoyant ses instructions au jeu.

    Paramètres
    ----------
    name : string
        nom du joueur
    species : Species
        Espèce que le joueur manipule
    game : Game
        Objet Game auquel le joueur participe
    
    """
    def __init__(self, name, Game):
        self._name = name
        self._species = None
        self._game = Game
        self._game.send_name(name)
        self._game._load_initial_parameters()
        species_type, total_nb, depart = self._game.get_start_info()
        self._species = Species(species_type, total_nb, *depart)

    def move(self, moves_list):
        """
        Cette fonction prend en entrée une liste de mouvements à faire.

        Elle met à jour les groupes et envoie l'information à l'objet Game.

        Paramètres
        ----------
        moves_list : list of dictionnaries
            {
                'from_position':
                'number':
                'to_position':
            }
        """
        for move in moves_list:
            group = self._species.get_group(move['from_position'])
            if group.get_size() == move['number']:
                group.move(move['to_position'])
                group.increase_size(self._game.get_map()[move['to_position'][0],move['to_position'][1]][0])
            elif group.get_size() > move['number']:
                pass
            else:
                raise ValueError('You cannot move {} {}, the group on ({}) has a size of {}'.format(move['number'], self._type, move['from_position'], group.get_size()))
        self._game.send_move(moves_list)

    def get_species(self):
        return self._species
