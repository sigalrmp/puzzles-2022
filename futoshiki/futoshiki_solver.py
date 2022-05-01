from futoshiki_util import *
from futoshiki_checker import *

def first_empty(board):
    num_board = board[board_type.NUM]
    for r in range_len(num_board):
        for c in range_len(num_board):
            if num_board[r][c] == 0:
                return (r, c)

def solve(board):
    if full(board):
        return board
    (r, c) = first_empty(board)
    space_opts = rand_space_options(board, r, c)
    for n in space_opts:
        copy = copy_board(board)
        copy[board_type.NUM][r][c] = n
        solution = solve(copy)
        if not solution is None:
            return solution

def valid(board):
    sols_count = [0] # why wont it let me use them further in? why does it need to be a list?
    too_many_sols = [False]
    def rec(rboard):
        sc = sols_count
        ts = too_many_sols
        if not ts[0]:
            if full(rboard):
                sc[0] += 1
                if sc[0] > 1:
                    ts[0] = True
            else:
                (r, c) = first_empty(rboard)
                space_opts = space_options(rboard, r, c)
                for n in space_opts:
                    copy = copy_board(rboard)
                    copy[board_type.NUM][r][c] = n
                    solution = rec(copy)
                    if not solution is None:
                        return solution
    rec(board)
    return sols_count[0] == 1