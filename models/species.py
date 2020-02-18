from .group import Group

class Species:
    """
    Cette classe représente une espèce, controllée par un Player.

    Elle contient un attribue groups qui contient l'ensemble des groupes d'une même espèce

    Paramètres
    ----------
    type : string
        type de l'espèce
    groups : list of Group
        liste contenant les différents groupes de l'espèce
    """

    def __init__(self, type, total_nb, position_x, position_y):
        self._type = type
        self._groups = [Group(total_nb, position_x, position_y)]

    def get_type(self):
        return self._type

    def get_groups(self):
        return self._groups

    def get_group(self, coordinates):
        """ 
        Renvoie un groupe situé à une coordonnée particulière 

        Paramètres
        ----------
        coordinates : list
            list de taille 2 contenant les coordonnées du groupe souhaité
        """
        for group in self.get_groups():
            if group.get_position() == coordinates:
                return group
        raise ValueError('No group is on the position ({},{})'.format(x,y))

    # def divise(self, group_1, nb1, nb2):
    #     group_1.change_size(nb1)
    #     self._groups.append(Group(nb2, group_1.get_position()[0], group_1.get_position()[1]))

    # def merge(self, group_1, group_2):
    #     self._groups.remove(group_1)
    #     self._groups.remove(group_2)
    #     self._groups.append(Group(group_1.get_size() + group_2.get_size(), group_1.get_position()[0], group_1.get_position()[1]))