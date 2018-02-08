from board import Board
from alphabeta import iterative_alpha_beta
from .helpers import run_move_seq


def test_winning_move_X():
    def stupid_h(state):
        return 0

    win_in_one = [(1, 1), (0, 0),
                  (0, 1), (2, 2)]
    b = run_move_seq(win_in_one, size=3, run_len=3)
    print(b)
    m = iterative_alpha_beta(b, stupid_h, max_seconds=1, max_depth=10)
    assert m == (2, 1)

def test_winning_move_O():
    def stupid_h(state):
        return 0

    win_in_one = [(0, 0), (1, 1),
                  (2, 2), (0, 1),
                  (1, 2)]
    b = run_move_seq(win_in_one, 3, 3)
    print(b)
    m = iterative_alpha_beta(b, stupid_h, max_seconds=1, max_depth=10)
    assert m == (2, 1)


def test_winning_move_X2():
    def stupid_h(state):
        return 0
    b = run_move_seq([(0, 1), (0,0), (2, 1), (2, 2)], 3, 3)
    print(b)

    m = iterative_alpha_beta(b, stupid_h, max_seconds=1, max_depth=10)
    assert m == (1, 1)