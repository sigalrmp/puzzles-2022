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

def solve(board):
    if full(board):
        return board
    row = None
    col = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                row = r
                col = c
                break
    space_opts = space_options_shuffled(board, row, col)
    for i in space_opts:
        copy = copy_board(board)
        copy[row][col] = i
        solution = solve(copy)
        if not solution is None:
            return solution

# clean this up it's terrible

def valid(board):
    if full(board):
        print('board is already finished')
    else: return valid_h(board, 0) == 1

def valid_h(board, sols):
    if full(board):
        return 1
    if sols is False:
        return sols
    if sols > 1:
        return False
    row = None
    col = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                row = r
                col = c
                break
    space_opts = space_options_shuffled(board, row, col)
    for i in space_opts:
        copy = copy_board(board)
        copy[row][col] = i
        solution = valid_h(copy, 0)
        if solution is False: return False
        if not solution is None:
            if solution > 1: return False
            else: sols += solution
    return sols