from futoshiki_util import *
from futoshiki_solver import *
from futoshiki_human_solver import *
from enum import Enum

def empty_board(len):
    num = empty_grid_list(len, len)
    hor_ineq = empty_grid_list(len, len - 1)
    ver_ineq = empty_grid_list(len - 1, len)
    return { board_type.NUM: num,
             board_type.HOR_INEQ: hor_ineq,
             board_type.VER_INEQ: ver_ineq }

def rand_full_board(len):
    empty = empty_board(len)
    rand_nums = solve(empty)
    return changed_obj(rand_nums, fill_in_ineqs)

def gen_board_h(board, depth, diff=None):
    l = board_len(board)
    if depth == 0:
        return board
    else:
        for i in shuffled_list_range(space_count(l)):
            (b, r, c) = tog_to_sep_index(i, l)
            new_board = copy_board(board)
            new_board[b][r][c] = 0
            v = valid(new_board) if diff is None else solve_like_human(new_board, diff)
            if v:
                # if not valid_check(board):
                    # print('valid (or valid_check) is not working')
                # else:
                return gen_board_h(new_board, depth - 1, diff)
    return board

def gen_board_generic(len):
    return gen_board_h(rand_full_board(len), 2 * len ** 2)

def valid_check(board):
    sol_1 = solve(board)
    for i in range(10):
        next_sol = solve(board)
        if not next_sol == sol_1:
            return False
    return True

def gen_board_graded(l, diff):
    return gen_board_h(rand_full_board(l), 2 * (space_count(l) - floor(l / 2)), diff)
