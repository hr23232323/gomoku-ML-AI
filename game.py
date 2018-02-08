from abc import ABC, abstractmethod
from itertools import cycle
from board import Board


class Game(object):
    def __init__(self, player_1, player_2, size=15, run_len=5):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = Board.empty(size, run_len)
        self.observers = []

    def start(self):
        for player in cycle((self.player_1, self.player_2)):
            move = player.move(self.board)

            self.board = self.board.after(move)

            for observer in self.observers:
                observer.on_move(self.board)

            if self.board.is_terminal:
                for observer in self.observers:
                    observer.on_end(self.board)
                break

    def register_observer(self, observer):
        self.observers.append(observer)


class Player(ABC):
    @abstractmethod
    def move(self, board):
        pass


class GameObserver(object):
    def on_move(self, board):
        pass

    def on_end(self, board):
        pass


class Announcer(GameObserver):
    def on_move(self, board):
        print(board)
        print()

    def on_end(self, board):
        print((None, 'Black', 'White')[board.winner] + " won!")
