from time import time
from game import Player
from registry import register


def negamax(state, heuristic, max_depth=10, max_seconds=9):
    start_time = time()
    def negamax_search(state, alpha, beta, depth):
        if depth == 0:
            return heuristic(state)
        if state.is_terminal:
            return float('inf') * state.winner
        best_value = -float('inf')
        for move in state.moves:
            next_state = state.after(move)
            val = negamax_search(next_state, -beta, -alpha, depth - 1) * -1
            best_value = max(best_value, val)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return best_value
    
    best_move = None
    best_score = -float('inf')
    for depth in range(1, max_depth):
        if time() - start_time > max_seconds:
            break
        for move in state.moves:
            next_state = state.after(move)
            score = negamax_search(next_state, -float('inf'), float('inf'), depth) * state.next_player
            if score > best_score:
                best_score, best_move = score, move

    return best_move



@register('nm')
class NegamaxPlayer(Player):
    def __init__(self, heuristic, max_depth=10, max_seconds=9):
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.max_seconds = max_seconds
    def move(self, state):
        return negamax(state, self.heuristic, self.max_depth, self.max_seconds)