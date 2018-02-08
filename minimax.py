from operator import itemgetter
from board import Stone
from registry import register
from game import Player

def minimax(state, heuristic):
    print("Running minimax...")
    def _play(state, maximizing):
        if state.over:
            return heuristic(state)
        selector = max if maximizing else min
        return selector((_play(state.after(move), not maximizing) for move in state.moves()))

    return max(
        ((move, _play(state.after(move), True)) for move in state.moves()),
        key=itemgetter(1)
    )

@register('minimax')
class MinimaxPlayer(Player):
    def __init__(self, heuristic):
        self.heuristic = heuristic
    def move(self, game_state):
        return minimax(game_state, self.heuristic)[0]
