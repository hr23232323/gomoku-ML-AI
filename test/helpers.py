from board import Board

def run_move_seq(seq, size=15, run_len=5):
    b = Board.empty(size, run_len)
    for move in seq:
        b = b.after(move)
    return b