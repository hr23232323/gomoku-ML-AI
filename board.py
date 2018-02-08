import numpy as np
from enum import IntEnum


class Stone(IntEnum):
    white = -1    
    empty = 0
    black = 1


class Board(object):
    __slots__ = ('grid', 'size', 'run', 'last_move', 'next_player', 'turn_count',
                 '_successors', '_winner', '_moves', '_is_terminal', '_is_full')
    def __init__(self, grid, size, run, last_move, next_player, turn_count):
        self.grid = grid
        self.size = size 
        self.run = run
        self.last_move = last_move
        self.next_player = next_player
        self.turn_count = turn_count

        self._successors = None
        self._winner = None
        self._moves = None
        self._is_terminal = None
        self._is_full = None

    @classmethod
    def empty(cls, size=15, run=5):
        """Create a new empty board"""
        return cls(np.zeros((size, size), dtype=np.int8), size, run, None, Stone.black, 0)

    def after(self, move):
        if self.grid[move] != Stone.empty and self.turn_count != 1:
            raise ValueError('{} already has a stone in it.'.format(move))
        new_board = Board(self.grid.copy(), self.size, self.run, move, self.next_player * -1, self.turn_count + 1)
        new_board.grid[move] = self.next_player

        return new_board

    @property
    def moves(self):
        """Get a list of all valid moves for the `next_player`"""
        if self._moves is None:
            empty_spots = np.argwhere(self.grid == (self.grid if self.turn_count == 1 else 0))
            np.random.shuffle(empty_spots)
            self._moves = list(map(tuple, empty_spots))
        return self._moves 
    
    @property
    def winner(self):
        """Returns the winning stone number, or 0 if there is no winner"""
        if self._winner is None:
            self._winner = 0
            if not (self.last_move is None or self.turn_count < 2*self.run - 1):
                goal_stone = -1 * self.next_player
                dist = self.run - 1
                row, col = self.last_move
                
                # The furthest distance we can check in any direction
                max_down = min(self.size - row - 1, dist)
                max_up = min(row, dist)
                max_right = min(self.size - col - 1, dist)
                max_left = min(col, dist)

                # The furthest we can check along the main diag
                max_dr = min(max_down, max_right)
                max_ul = min(max_up, max_left)

                # The furthest we can check along the anti-diag
                max_dl = min(max_down, max_left)
                max_ur = min(max_up, max_right)

                # Check the columns
                stones_up = 0
                for offset in range(1, max_up + 1):
                    if self.grid[row - offset][col] == goal_stone:
                        stones_up += 1
                    else:
                        break
                stones_down = 0
                for offset in range(1, max_down + 1):
                    if self.grid[row + offset][col] == goal_stone:
                        stones_down += 1
                    else:
                        break
                if stones_up + stones_down + 1 == self.run:
                    self._winner = goal_stone
                    return goal_stone

                # Check the rows
                stones_left = 0
                for offset in range(1, max_left + 1):
                    if self.grid[row][col - offset] == goal_stone:
                        stones_left += 1
                    else:
                        break
                stones_right = 0
                for offset in range(1, max_right + 1):
                    if self.grid[row][col + offset] == goal_stone:
                        stones_right += 1
                    else:
                        break
                if stones_left + stones_right + 1 == self.run:
                    self._winner = goal_stone
                    return goal_stone

                # Check the main diag
                stones_ul = 0
                for offset in range(1, max_ul + 1):
                    if self.grid[row - offset][col - offset] == goal_stone:
                        stones_ul += 1
                    else:
                        break
                stones_dr = 0
                for offset in range(1, max_dr + 1):
                    if self.grid[row + offset][col + offset] == goal_stone:
                        stones_dr += 1
                    else:
                        break
                if stones_ul + stones_dr + 1 == self.run:
                    self._winner = goal_stone
                    return goal_stone

                # Check the anti diag (left to right)
                stones_ur = 0
                for offset in range(1, max_ur + 1):
                    if self.grid[row - offset][col + offset] == goal_stone:
                        stones_ur += 1
                    else:
                        break
                stones_dl = 0
                for offset in range(1, max_dl + 1):
                    if self.grid[row + offset][col - offset] == goal_stone:
                        stones_dl += 1
                    else:
                        break
                if stones_ur + stones_dl + 1 == self.run:
                    self._winner = goal_stone
                    return goal_stone

        return self._winner

    @property
    def is_full(self):
        """Check if the board is full"""
        if self._is_full is None:
            self._is_full = np.sum(np.abs(self.grid)) == self.size ** 2
        return self._is_full
        

    @property
    def is_terminal(self):
        """Check if no more moves can be made"""
        if self._is_terminal is None:
            self._is_terminal = self.is_full or self.winner
        return self._is_terminal

    @property
    def diag_sections(self):
        diags = [self.grid.diagonal(offset) for offset in range(-self.size + self.run, self.size - self.run - 1)] 
        t_diags = [self.grid.T.diagonal(offset) for offset in range(-self.size + self.run, self.size - self.run - 1)]
        return diags + t_diags

    @property
    def sections(self):
        return list(self.grid) + list(self.grid.T) + self.diag_sections

    def __getitem__(self, index):
        return self.grid[index]

    def __str__(self):
        return np.array2string(self.grid, formatter={'int': lambda x: ('_', 'X', 'O')[x]})
