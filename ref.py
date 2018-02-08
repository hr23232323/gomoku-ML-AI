from board import Stone
from game import Player, Game, GameObserver
from os import path, stat
from util import num_to_char, char_to_num
from time import sleep
from halo import Halo


class RefPlayer(Player):
    def __init__(self, team_name):
        self.team_name = team_name
        self.go_file_name = "{}.go".format(team_name)

    def move(self, game_state):
        # Make sure the ref has time to get rid of our go file so we don't jump the gun
        sleep(0.5)
        with Halo(text='Waiting for go file...', spinner='hamburger'):
            while not path.exists(self.go_file_name):
                sleep(0.05)

        # Read the other teams move from the board and play it
        with open('move_file', 'r') as move_file:
            _, col_letter, row = move_file.readline().split()
            return (int(row) - 1, char_to_num(col_letter))


class MoveWriter(GameObserver):
    def __init__(self, color, team_name):
        self.color = color
        self.team_name = team_name
        super().__init__()

    def on_move(self, state):
        last_move = state.last_move
        if state[last_move] == self.color:
            column_letter = num_to_char(last_move[1])
            row = last_move[0]
            with open('move_file', 'w') as move_file:
                move_file.write("{} {} {}\n".format(self.team_name, column_letter, row + 1))
                move_file.flush()

    def on_end(self, state):
        pass


class ReffedGame(Game):
    def __init__(self, player, team_name, size=15, run_len=5):
        ref_player = RefPlayer(team_name)
        self.team_name = team_name
        super().__init__(ref_player, player, size=size, run_len=run_len)

    def start(self):
        with Halo(text='Waiting for go file...', spinner='hamburger'):
            while not path.exists('{}.go'.format(self.team_name)):
                sleep(0.05)

        write_color = Stone.white
        # Check move file, if it's empty swap the players
        if stat('move_file').st_size == 0:
            print("We go first, swapping players....")
            write_color = Stone.black
            self.player_1, self.player_2 = self.player_2, self.player_1
        self.register_observer(MoveWriter(write_color, self.team_name))
        super().start()
