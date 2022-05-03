from sudoku_util import *
from sudoku_solver import valid
from sudoku_reliant_util import *
from sudoku_grader import *

def gen_board_h(board, depth):
    if depth == 0:
        return board
    else:
        for r in rand_places():
            for c in rand_places():
                new_board = copy_board(board)
                new_board[r][c] = 0
                if valid(new_board):
                    return gen_board_h(new_board, depth - 1)
    return board

def gen_board():
    return gen_board_h(rand_board(), 70, 0)

def gen_board_level_h(board, depth, diff):
    if depth == 0:
        return board
    else:
        for r in rand_places():
            for c in rand_places():
                new_board = copy_board(board)
                new_board[r][c] = 0
                notes = board_to_notes(new_board)
                if solve_like_human(notes, diff[0], diff[1], diff[2]):
                    return gen_board_level_h(new_board, depth - 1, diff)
    return board

def gen_board_level(diff):
    return gen_board_level_h(rand_board(), 200, diff)
