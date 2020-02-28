from .group import Group


class Specie:
    """
    This class represents a specie, controlled by a Player.

    It has a groups attribute that contain all the groups of a same specie.

    Parameters
    ----------
    type : string
        type de l'espèce
    total_nb : integer
        start number of specie
    position_x : integer
        x position of the start group
    position_y : integer
        y_position of the start group
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

        This function returns a particular group at a particular coordinates

        Parameters
        ----------
        coordinates : list
            size-2 list containing [x, y] coordinates
        """
        x, y = coordinates
        for group in self.get_groups():
            if group.get_position() == coordinates:
                return group
        raise ValueError("No group is on the position ({},{})".format(x, y))

    # def divide(self, group_1, nb1, nb2):
    #     group_1.change_size(nb1)
    #     self._groups.append(Group(nb2, group_1.get_position()[0], group_1.get_position()[1]))

    # def merge(self, group_1, group_2): self._groups.remove(group_1) self._groups.remove(group_2)
    # self._groups.append(Group(group_1.get_size() + group_2.get_size(), group_1.get_position()[0],
    # group_1.get_position()[1]))
