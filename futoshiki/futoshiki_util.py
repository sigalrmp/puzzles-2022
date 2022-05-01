from enum import Enum, auto
from math import floor
from random import shuffle

def gen_options(board_len):
    return list_range(min=1, max=board_len + 1)

class board_type(Enum):
    HOR_INEQ = auto()
    VER_INEQ = auto()
    NUM = auto


class difficulty(Enum):
    EASY = (1, 0, 0)
    MEDIUM = (10, 2, 2)
    HARD = (30, 5, 10)
    WICKED = (80, 10, 30)

def section_to_list(sect_pos, len):
    row = sect_pos[0]
    col = sect_pos[1]
    l = []
    if col is False: # don't change this to (not col) or (row) bc python is annoying and (not 0) is True
        for i in range(len):
            l += [(row, i)]
    elif row is False:
        for i in range(len):
            l += [(i, col)]
    return l 

def all_sections(len):
    l = []
    for r in range(len):
        l += [(r, False)] # adds row r
    for c in range(len):
        l += [(False, c)] # adds col c
    return l

def board_len(board):
    return len(board[board_type.NUM])

def rand_options(len):
    r = list_range(min=1, max=len + 1)
    shuffle(r)
    return r

def copy_board(board):
    new_num = copy_2d_list(board[board_type.NUM])
    new_hor_ineq = copy_2d_list(board[board_type.HOR_INEQ])
    new_ver_ineq = copy_2d_list(board[board_type.VER_INEQ])
    return {board_type.NUM: new_num, 
            board_type.HOR_INEQ: new_hor_ineq, 
            board_type.VER_INEQ: new_ver_ineq}

def space_to_char(board, min_board_type, row, col):
    space = board[min_board_type][row][col]
    if space == 0:
        if min_board_type == board_type.NUM:
            return '-'
        else: return ' '
    else: return str(space)

def board_to_str(board):
    s = ''
    l = board_len(board) 
    for r in range(2 * l - 1):
        for c in range(l):
            if r % 2 == 0: # normal numbers row
                s += space_to_char(board, board_type.NUM, int(r / 2), c)
                if c == l - 1:
                    if r < 2 * l - 2:
                        s += '\n'
                else: 
                    s += ' ' + space_to_char(board, board_type.HOR_INEQ, int(r / 2), c) + ' '
            else: # inequalities row
                s += space_to_char(board, board_type.VER_INEQ, int((r - 1) / 2), c)
                if c == l - 1:
                    s += '\n'
                else: s += '   '
    return s

def full(board):
    f = True
    for r in board[board_type.NUM]:
        for n in r:
            f = f and n > 0
    return f

def fill_in_ineqs_h(board, r_shift, c_shift):
    ineq_board = []
    l = board_len(board)
    for r in range(l - r_shift):
        ineq_row = []
        for c in range(l - c_shift):
            space_one = board[board_type.NUM][r][c]
            space_two = board[board_type.NUM][r + r_shift][c + c_shift]
            if space_one == 0 or space_two == 0:
                ineq_row += [0]
            elif space_one > space_two:
                ineq_row += ['>']
            elif space_one < space_two:
                ineq_row += ['<']
        ineq_board += [ineq_row]
    return ineq_board
                

def fill_in_ineqs(board):
    board[board_type.HOR_INEQ] = fill_in_ineqs_h(board, 0, 1)
    board[board_type.VER_INEQ] = fill_in_ineqs_h(board, 1, 0)

def tog_to_sep_index(i, l):
    # print('l: ' + str(l))
    # print('if ' + str(i) + ' < ' + str(l ** 2) + ', this should be num')
    # print('if ' + str(i) + ' < ' + str(2 * (l ** 2) - l) + ', this should be hor')
    # print('otherwise, this should be ver')
    if i < (l ** 2):
        # print('in num board')
        return (board_type.NUM, floor(i / l), i % l)
    elif i < (2 * (l ** 2) - l):
        hor_i = i - l ** 2
        # print('in hor ineq board')
        return (board_type.HOR_INEQ, floor(hor_i / (l - 1)), hor_i % (l - 1))
    else:
        # print('in ver ineq board')
        ver_i = i - 2 * (l ** 2) + l
        return (board_type.VER_INEQ, floor(ver_i / l), ver_i % l)

def space_count(len):
    return 3 * len ** 2 - 2 * len

def opp_ineq(ineq):
    if ineq == '<':
        return '>'
    if ineq == '>':
        return '<'
    return 0

def num_board_index_to_pos(i, l): # takes an index btwn 0 and l ^ 2 and returns the (r, c) pos in a board of length l
    return (floor(i / l), i % l)

def num_board_pos_to_index(p, l): # does the opposite of the previous function
    (r, c) = p
    return l * r + c

# functions that would be in util:

def changed_obj(o, f):
    f(o)
    return o

def copy_2d_list(l):
        copy = []
        for i in l:
            copy += [list.copy(i)]
        return copy

def range_len(iter):
    return range(len(iter))

def list_range(max, min=0):
    return list(range(min, max))

def grid_list_to_str(l):
    s = ''
    rows = len(l)
    cols = len(l[0])
    for r in range(rows):
        for c in range(cols):
            s += str(l[r][c])  
            if c < cols - 1:
                s += ' '
            elif r < rows - 1:
                s += '\n'
    return s

def empty_grid_list(rows, cols):
    l = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row += [0]
        l += [row]
    return l

def dict_to_str(dict):
    s = ''
    for key in dict:
        s += str(key) + ': ' + str(dict[key]) + '\n'
    return s

def shuffled_list_range(i):
    return changed_obj(list_range(i), shuffle)