class Group:
    def __init__(self, size, position_x, position_y):
        self._size = size
        self._position_x = position_x
        self._position_y = position_y

    def get_position(self):
        return [self._position_x,self._position_y]

    def get_size(self):
        return self._size

    def move(self, x, y):
        try:
            assert abs(x - self._position_x) <=1 and abs(y-self._position_y) <= 1
        except:
            raise ValueError('You moved the group too much')
        self._position_x = x
        self._position_y = y
    
    def increase_size(self, amount):
        self._size += amount 