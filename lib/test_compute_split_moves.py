from .util import get_neighbors, get_moves
from .compute_split_moves import (
    couple_size_split,
    compute_all_couple_targets,
    compute_all_possible_moves_for_one_group,
)


def test_couple_size_split():
    couples_size = couple_size_split(size=4)
    assert couples_size == [(3, 1), (2, 2), (1, 3)]


def test_get_neighbors():
    next_positions = get_neighbors(cell=(0, 0), shape=(3, 3), with_start_position=True)
    assert next_positions == [(0, 1), (1, 0), (1, 1), (0, 0)]
    next_positions = get_neighbors(cell=(1, 1), shape=(3, 3), with_start_position=True)
    assert next_positions == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
        (1, 1),
    ]


def test_compute_all_couple_targets():
    next_positions = get_neighbors(cell=(0, 0), shape=(3, 3), with_start_position=True)
    couple_targets = compute_all_couple_targets(next_positions)
    assert couple_targets == [
        ((0, 1), (1, 0)),
        ((0, 1), (1, 1)),
        ((0, 1), (0, 0)),
        ((1, 0), (1, 1)),
        ((1, 0), (0, 0)),
        ((1, 1), (0, 0)),
    ]


def test_get_moves_without_split():
    next_positions = get_neighbors(cell=(0, 0), shape=(3, 3), with_start_position=True)
    moves_without_split = get_moves((0, 0), 1, next_positions)
    assert next_positions == [(0, 1), (1, 0), (1, 1), (0, 0)]
    assert moves_without_split == [
        (0, 0, 1, 0, 1),
        (0, 0, 1, 1, 0),
        (0, 0, 1, 1, 1),
        (0, 0, 1, 0, 0),
    ]


def test_compute_all_possible_moves_for_one_group():
    moves = compute_all_possible_moves_for_one_group(size=2, cell=(0, 0), shape=(3, 3))
    assert moves == [
        [(0, 0, 2, 0, 1)],
        [(0, 0, 2, 1, 0)],
        [(0, 0, 2, 1, 1)],
        [(0, 0, 2, 0, 0)],
        [(0, 0, 1, 0, 1), (0, 0, 1, 1, 0)],
        [(0, 0, 1, 0, 1), (0, 0, 1, 1, 1)],
        [(0, 0, 1, 0, 1)],
        [(0, 0, 1, 1, 0), (0, 0, 1, 1, 1)],
        [(0, 0, 1, 1, 0)],
        [(0, 0, 1, 1, 1)],
    ]
