import pytest
from board import Board, Stone
from .helpers import run_move_seq


def won_games():
    col_win = [(3, 3), (3, 4), 
               (4, 3), (4, 4), 
               (5, 3), (5, 4),
               (6, 3), (6, 4),
               (7, 3)]
    
    row_win = [(3, 3), (4, 3),
               (3, 4), (4, 4),
               (3, 5), (4, 5),
               (3, 6), (4, 6),
               (3, 7)]

    diag_win = [(0, 0), (14, 14),
                (1, 1), (10, 10),
                (2, 2), (9, 5),
                (3, 3), (8, 7),
                (4, 4)]
    
    anti_diag_win = [(1, 6), (14, 14),
                     (2, 5), (13, 12),
                     (3, 4), (13, 11),
                     (4, 3), (10, 10),
                     (5, 2)]

    yield run_move_seq(col_win)
    yield run_move_seq(row_win)
    yield run_move_seq(diag_win)
    yield run_move_seq(anti_diag_win)
    
@pytest.mark.parametrize("game", won_games())
def test_winners(game):
    print(game)
    assert game.winner == Stone.black

def test_take_move():
    b = run_move_seq([(1, 1), (1, 1)], 3, 3)
    assert b.grid[1][1] == -1

def test_take_move_twice_fail():
    with pytest.raises(ValueError):
        run_move_seq([(1, 1), (1, 1), (1, 1)])


    