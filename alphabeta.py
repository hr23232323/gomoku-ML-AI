from time import time
from board import Stone
from game import Player
from registry import register

def iterative_alpha_beta(state, heuristic, max_depth=10, max_seconds=8):
    start_time = time()

    def alpha_beta_search(state, alpha, beta, depth):
        def min_value(state, alpha, beta, depth):
            val = float('inf')

            for move in state.moves_to_check:
                next_state = state.after(move)
                val = min(val, alpha_beta_search(next_state, alpha, beta, depth - 1))
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return val

        def max_value(state, alpha, beta, depth):
            val = -float('inf')

            for move in state.moves_to_check:
                next_state = state.after(move)
                val = max(val, alpha_beta_search(next_state, alpha, beta, depth - 1))
                alpha = max(alpha, val)                
                if beta <= alpha:
                    break
            return val

        if state.is_terminal:
                return state.winner * float('inf')
        
        if depth <= 0 or time() - start_time >= max_seconds:
            return heuristic(state)
        
        if state.next_player == Stone.black:  # If last move is None this still works
            return max_value(state, alpha, beta, depth)
        
        else:
            return min_value(state, alpha, beta, depth)

    best_move = None
    val = -float('inf')
    for depth in range(1, max_depth):  # TODO: cache results
        if time() - start_time > max_seconds:
            break
        for move in state.moves_to_check:
            next_state = state.after(move)
            score = alpha_beta_search(next_state, -float('inf'), float('inf'), depth) * state.next_player

            if score > val:
                val, best_move = score, move
    return best_move


@register('ab')
class AlphaBetaPlayer(Player):
    def __init__(self, heuristic, max_depth=10, max_seconds=2):
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.max_seconds = max_seconds
    def move(self, board):
        #print('move from alpha beta called')
        return iterative_alpha_beta(board, self.heuristic, self.max_depth, self.max_seconds)
