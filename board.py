import numpy as np
from enum import IntEnum


class Stone(IntEnum):
    white = -1    
    empty = 0
    black = 1


class Board(object):
    __slots__ = ('grid', 'size', 'run', 'last_move', 'next_player', 'turn_count',
                 '_successors', '_winner', '_moves', '_is_terminal', '_is_full', '_moves_to_check')
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
        self._moves_to_check = None

    @classmethod
    def empty(cls, size=15, run=5):
        """Create a new empty board"""
        return cls(np.zeros((size, size), dtype=np.int8), size, run, None, Stone.black, 0)

    def after(self, move):
        if move is None:
            raise ValueError('None passed')
        #print(self.grid[move])
        if self.grid[move] != Stone.empty and self.turn_count != 1:
            raise ValueError('{} already has a stone in it.'.format(move))
        new_board = Board(self.grid.copy(), self.size, self.run, move, self.next_player * -1, self.turn_count + 1)
        new_board.grid[move] = self.next_player

        return new_board

    def position_value(self, move):
        """Get the value of stone (white, black, empty) at a certain location"""
        return self.grid[move]

    @property
    def moves(self):
        """Get a list of all valid moves for the `next_player`"""
        if self._moves is None:
            #print('inside loop of moves')
            empty_spots = np.argwhere(self.grid == (self.grid if self.turn_count == 1 else 0))
            #print('size', empty_spots.size)
            np.random.shuffle(empty_spots)
            self._moves = list(map(tuple, empty_spots))
        return self._moves 

    @property
    def moves_to_check(self):
        if self._moves_to_check is None:
            taken_spots = np.argwhere(self.grid != (self.grid if self.turn_count == 1 else 0))
            np.random.shuffle(taken_spots)


            # define a 3x3 mask
            # put on mask on every element inside empty spots while no index error
            area_mask = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
            interesting_moves = []

            if (taken_spots.size != 0):
                for i in range(taken_spots.size//2):
                    for value in area_mask:
                        current_position = value + taken_spots[i]
                        if(not self.out_of_bounds(current_position[0], current_position[1])):
                            continue
                        
                        if(self.__getitem__(current_position[0], [current_position[1]]) == Stone.empty):
                            interesting_moves.append(value + taken_spots[i])
            else:
                interesting_moves = Board.moves.__get__(self)

            #print(interesting_moves)
            self._moves_to_check = list(map(tuple, interesting_moves))

        return self._moves_to_check

    def out_of_bounds(self, index0, index1):
        counter = True 
        #print(index0, index1)

        if(index0 < 0 or index0 > 14 or index1 < 0 or index1 > 14):
            counter = False

        return counter

    
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

    def __getitem__(self, index0, index1):
        return self.grid[index0][index1]

    def __str__(self):
        return np.array2string(self.grid, formatter={'int': lambda x: ('_', 'X', 'O')[x]})
