from enum import Enum
from sudoku_util import *
from sudoku_solver import valid
from sudoku_reliant_util import *
from sudoku_grader import *

def gen_board_h(board, depth, level):
    if level == depth:
        return board
    else:
        for r in rand_places():
            for c in rand_places():
                new_board = copy_board(board)
                new_board[r][c] = 0
                if valid(new_board):
                    return gen_board_h(new_board, depth, level + 1)
    return board

def gen_board():
    return gen_board_h(rand_board(), 70, 0)

def gen_board_level_h(board, depth, level, easyness):
    if level == depth:
        return board
    else:
        for r in rand_places():
            for c in rand_places():
                new_board = copy_board(board)
                new_board[r][c] = 0
                notes = board_to_notes(board)
                if solve_like_human(notes, easyness[0], easyness[1], easyness[2]):
                    return gen_board_h(new_board, depth, level + 1)
    return board

def gen_board_level(easyness):
    return gen_board_level_h(rand_board(), 70, 0, easyness)