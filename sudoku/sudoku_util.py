# from sudoku_solver import solve
from random import shuffle
from math import floor

def copy_board(board):
    copy = []
    for i in board:
        copy += [list.copy(i)]
    return copy

def copy_notes(notes):
    copy = {}
    # print('notes:\n' + notes_to_str(notes))
    for s in notes:
        # print('s: ' + str(s))
        if not type(notes[s]) is list:
            print('wtf. s: ' + str(s) + ', notes[s]: ' + str(notes[s]))
        copy.update({s: list.copy(notes[s])}) 
    return copy

def gen_options():
    return list(range(1, 10))

def board_to_str(board):
    s = ''
    for r in range(9):
        for c in range(9):
            if not(c == 0): s += ' '
            space = board[r][c]
            if space == 0:
                space = '-'
            s += str(space)
            if c == 8:
                if r % 3 == 2: s += '\n'
                s += '\n'
            elif c % 3 == 2:
                s += '  '
    return s

def notes_to_str(notes): # this is really awful fix it
    s = ''
    for r in range(9):
        for c in range(9):
            s += str((r, c)) + ': ' + str(notes[(r, c)]) + '\n'
    return s

def section_to_list(row, col): # if it's a row, col should be False (and vise versa)
    l = []
    if col is False: # it's a row
        for i in range(9):
            l += [(row, i)]
    elif row is False: # it's a col
        for i in range(9):
            l += [(i, col)]
    else: # it's a box
        for i in range(9):
            l += [(3 * row + i % 3, 3 * col + floor(i / 3))]
    return l

def all_sections():
    l  = []
    for r in range(9):
        l += [(r, False)] # adds row r
    for c in range(9):
        l += [(False, c)] # adds col c
    for br in range(3):
        for bc in range(3):
            l += [(br, bc)] # adds box (br, bc)
    return l

def empty_board():
    board = []
    for r in range(9): # better way to do this? iter?
        row = []
        for c in range(9):
            row += [0]
        board += [row]
    return board

def full(board):
    is_full = True
    for r in board:
        for i in r:
            is_full = is_full and i > 0
    return is_full

def rand_fillers(): # generates a list with the integers from 0 to 10 in a random order
    r = list(range(1, 10))
    shuffle(r)
    return r

def rand_places():
    r = list(range(0, 9))
    shuffle(r)
    return r

def check_row(board, row):
    def rec(c, p):
        if c == 9:
            return True
        else:
            space = board[row][c]
            if space == 0:
                return rec(c + 1, p)
            elif space in p:
                list.remove(p, space)
                return rec(c + 1, p)
            else:
                return False
    return rec(0, gen_options())

def check_col(board, col):
    def rec(r, p):
        if r == 9: 
            return True
        else:
            space = board[r][col]
            if space == 0:
                return rec(r + 1, p)
            elif space in p:
                list.remove(p, space)
                return rec(r + 1, p)
            else:
                return False
    return rec(0, gen_options())

def check_box(board, b_row, b_col):
    def rec(i, p):
        if i == 9:
            return True
        else:
            l_row = floor(i / 3)
            l_col = i % 3
            row = 3 * b_row + l_row
            col = 3 * b_col + l_col
            space = board[row][col]
            if space == 0:
                return rec(i + 1, p)
            elif space in p:
                list.remove(p, space)
                return rec(i + 1, p)
            else:
                return False
    return rec(0, gen_options())

def check_space(board, row, col):
    box_row = floor(row / 3)
    box_col = floor(col / 3)
    return check_row(board, row) and \
        check_col(board, col) and \
        check_box(board, box_row, box_col)

def space_options(board, row, col):
    all_opts = range(1, 10)
    space_opts = []
    for i in all_opts:
        b = copy_board(board)
        b[row][col] = i
        if check_space(b, row, col):
            space_opts += [i]
    return space_opts