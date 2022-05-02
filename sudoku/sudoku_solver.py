import cProfile
from sudoku_util import *
possibilities = []

possibilities = gen_options()
# print('possibilities: ' + str(possibilities))

def space_options_shuffled(board, row, col):
    rand = rand_fillers()
    space_opts = []
    for i in rand:
        b = copy_board(board)
        b[row][col] = i
        if check_space(b, row, col):
            space_opts += [i]
    return space_opts

def first_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)

def solve(board):
    if full(board):
        return board
    (row, col) = first_empty(board)
    space_opts = space_options_shuffled(board, row, col)
    for i in space_opts:
        copy = copy_board(board)
        copy[row][col] = i
        solution = solve(copy)
        if not solution is None:
            return solution

def valid(board):
    sols_count = [0]
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
                    copy[r][c] = n
                    solution = rec(copy)
                    if not solution is None:
                        return solution
    rec(board)
    return sols_count[0] == 1