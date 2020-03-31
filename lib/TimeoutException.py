from typing import Tuple


class TimeoutException(Exception):
    def __init__(self, moves: Tuple[Tuple[int, int, int, int, int], ...]):
        self.moves = moves
