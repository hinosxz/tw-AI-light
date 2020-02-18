from group import Group

class Species:

    def __init__(self, type, total_nb, position_x, position_y):
        self._type = type
        self._groups = [Group(total_nb, position_x, position_y)]
        self._total_nb = total_nb

    def get_type(self):
        return self._type

    def get_groups(self):
        return self._groups

    def get_group(self, x, y):
        for group in self.get_groups():
            if group.get_position() == [x,y]:
                return group
        raise ValueError('No group is on the position ({},{})'.format(x,y))

    # def divise(self, group_1, nb1, nb2):
    #     group_1.change_size(nb1)
    #     self._groups.append(Group(nb2, group_1.get_position()[0], group_1.get_position()[1]))

    # def merge(self, group_1, group_2):
    #     self._groups.remove(group_1)
    #     self._groups.remove(group_2)
    #     self._groups.append(Group(group_1.get_size() + group_2.get_size(), group_1.get_position()[0], group_1.get_position()[1]))