from futoshiki_util import *
# from .. import Util

# checking methods
#   check_section_repetition(nums_board, section)
#       section is iterable of positions of number spaces in the section
#       generate list of options (using util gen_options())
#       go through spaces in section and for each, if it has a number, take that number out
#   check_hor_inequalities(board)
#       board is dictionary with entries for the 'num' board and the ineq boards
#       go through each ineq in board[hor_ineq]

def check_section_repitition(board, section): # nums_board has the numbers, sect has the positions
    l = board_len(board)
    # print('section: ' + str(section) + ', len: ' + str(l))
    section_list = section_to_list(sect_pos=section, len=l)
    nums_board = board[board_type.NUM]
    l = board_len(board)
    def rec(i, opts):
        if i == l:
            return True
        else:
            space_pos = section_list[i]
            # print('space_pos: ' + str(space_pos))
            space = nums_board[space_pos[0]][space_pos[1]]
            if space == 0:
                return rec(i + 1, opts)
            elif space in opts:
                list.remove(opts, space)
                return rec(i + 1, opts)
            else:
                return False
    return rec(0, gen_options(l)) # gen_options(l))

def check_repitition(board):
    valid = True
    l = board_len(board)
    sections = all_sections(l)
    for section in sections:
        valid = valid and check_section_repitition(board, section)
    return valid

def check_row_hor_inequalities(board, row):
    valid = True
    for c in range_len(board[board_type.HOR_INEQ][0]):
        space_one = board[board_type.NUM][row][c]
        space_two = board[board_type.NUM][row][c + 1]
        ineq_opp = board[board_type.HOR_INEQ][row][c]
        if not (space_one == 0 or space_two == 0):
            if ineq_opp == '>':
                valid = valid and space_one > space_two
            elif ineq_opp == '<':
                valid = valid and space_one < space_two
    return valid

def check_hor_inequalities(board):
    valid = True
    for r in range_len(board[board_type.HOR_INEQ]):
        valid = valid and check_row_hor_inequalities(board, r)
    return valid

def check_col_ver_inequalities(board, col):
    valid = True
    for r in range_len(board[board_type.VER_INEQ]):
        space_one = board[board_type.NUM][r][col]
        space_two = board[board_type.NUM][r + 1][col]
        ineq_opp = board[board_type.VER_INEQ][r][col]
        if not (space_one == 0 or space_two == 0):
            if ineq_opp == '>':
                valid = valid and space_one > space_two
            elif ineq_opp == '<':
                valid = valid and space_one < space_two
    return valid

def check_ver_inequalities(board):
    valid = True
    for c in range_len(board[board_type.VER_INEQ][0]):
        valid = valid and check_col_ver_inequalities(board, c)
    return valid

# when you come back to look at this, make sure you find a way to consolidate the ver and hor checks into one

# okay so I wrote the check_board using checks because I felt like it but it's definitely worse right?

# checks = (check_repitition, check_hor_inequalities, check_ver_inequalities)

def check_board(board):
    # valid = True
    # for check in range_len(checks):
    #     valid = valid and checks[check](board)
    # return valid
    return check_repitition(board) and check_hor_inequalities(board) and check_ver_inequalities(board)

def check_space(board, row, col):
    return check_section_repitition(board, (row, False)) and \
           check_section_repitition(board, (False, col)) and \
           check_row_hor_inequalities(board, row) and \
           check_col_ver_inequalities(board, col)

def space_options(board, row, col): # should this be a position (r, c) instead? also is it necessary at all for solving?
    all_opts = gen_options(board_len(board))
    space_val = board[board_type.NUM][row][col]
    if space_val > 0:
        return [space_val]
    space_opts = []
    for n in all_opts:
        b = copy_board(board)
        b[board_type.NUM][row][col] = n
        if check_space(b, row, col):
            space_opts += [n]
    return space_opts

def rand_space_options(board, row, col):
    return changed_obj(space_options(board, row, col), shuffle)