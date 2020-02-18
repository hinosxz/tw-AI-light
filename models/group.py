class Group:
    """
    Groupe d'entité faisant partie d'une espèce

    Cette classe sert à représenter un groupe d'une espèce donnée, et de récupérer facilement
    ses informations.

    Paramètres
    ----------
    size : integer
        taille du groupe
    position_x : integer
        indice de ligne du groupe
    position_y : integer
        indice de colonne du groupe

    Attributs (objets)
    ---------
    size : integer
        taille du groupe
    position_x : integer
        indice de ligne du groupe
    position_y : integer
        indice de colonne du groupe

    """
    
    def __init__(self, size, position_x, position_y):
        self._size = size
        self._position_x = position_x
        self._position_y = position_y

    def get_position(self):
        return [self._position_x,self._position_y]

    def get_size(self):
        return self._size

    def move(self, coordinates):
        x, y = coordinates
        try:
            assert abs(x - self._position_x) <=1 and abs(y-self._position_y) <= 1
        except:
            raise ValueError('You moved the group too much')
        self._position_x = x
        self._position_y = y
    
    def increase_size(self, amount):
        
        self._size += amount 

if __name__ == '__main__':
    print(Group.__doc__)