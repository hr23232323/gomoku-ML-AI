from game import Game, Announcer
from ref import ReffedGame
from registry import REGISTERED_HEURISTICS, REGISTERED_PLAYERS
import heuristic
import fire

import alphabeta

class Local(object):
    def __init__(self, h1, a1, h2, a2, size=15, run_len=5):
        self._h1 = h1
        self._h2 = h2
        self._a1 = a1
        self._a2 = a2
        self._size = size
        self._run_len = run_len

    def start(self):
        h1 = REGISTERED_HEURISTICS[self._h1]
        a1 = REGISTERED_PLAYERS[self._a1]
        p1 = a1(h1)

        h2 = REGISTERED_HEURISTICS[self._h2]
        a2 = REGISTERED_PLAYERS[self._a2]
        p2 = a2(h2)

        game = Game(p1, p2, size=self._size, run_len=self._run_len)
        game.register_observer(Announcer())
        game.start()


class Reffed(object):
    def __init__(self, h, a, team_name, size=15, run_len=5):
        self._h = h
        self._team_name = team_name
        self._a = a
        self._size = size
        self._run_len = run_len

    def start(self):
        h = REGISTERED_HEURISTICS[self._h]
        a = REGISTERED_PLAYERS[self._a]
        game = ReffedGame(a(h), self._team_name, size=self._size, run_len=self._run_len)
        game.register_observer(Announcer())
        game.start()


def main():
    fire.Fire({
        'local': Local, 
        'reffed': Reffed, 
        'algorithms': list(REGISTERED_PLAYERS.keys()), 
        'heuristics': list(REGISTERED_HEURISTICS.keys()),
        })


if __name__ == '__main__':
    main()
