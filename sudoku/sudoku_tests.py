from sudoku_solver import *
from sudoku_util   import *
from sudoku_generator import *
from sudoku_grader import *
from doctest import *

test_board = [[0, 1, 0,   0, 0, 0,   0, 0, 0], 
              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],

              [0, 0, 0,   1, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   1, 0, 0],

              [0, 0, 0,   0, 0, 0,   0, 0, 0],
              [0, 0, 1,   0, 0, 0,   0, 0, 0],
              [0, 0, 0,   0, 0, 0,   0, 0, 0]]

full_test_board = [[1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],

                   [1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],

                   [1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],
                   [1, 2, 3,    4, 5, 6,    7, 8, 9],]

other_test_board = [[0, 0, 1,    0, 0, 6,    3, 0, 0],
                    [0, 3, 0,    8, 0, 0,    7, 2, 0],
                    [0, 0, 0,    4, 0, 0,    0, 0, 0],

                    [0, 1, 0,    0, 0, 0,    0, 0, 9],
                    [9, 0, 0,    7, 3, 0,    1, 0, 0],
                    [6, 0, 0,    0, 0, 0,    5, 0, 0],

                    [1, 9, 5,       0, 0, 0,    0, 0, 0],
                    [0, 0, 7,       0, 0, 8,    0, 0, 0],
                    [0, 0, 0,       1, 0, 0,    0, 0, 4]]
        
another_test_board = [[4, 5, 0,    3, 0, 7,    6, 0, 1],
                      [0, 0, 7,    0, 0, 0,    0, 9, 5],
                      [6, 3, 0,    0, 2, 5,    0, 0, 8],

                      [2, 0, 0,    8, 0, 0,    0, 1, 0],
                      [0, 0, 0,    0, 0, 0,    0, 3, 2],
                      [0, 0, 0,    2, 0, 1,    0, 0, 6],

                      [0, 0, 8,    0, 7, 2,    0, 6, 0],
                      [3, 0, 2,    0, 6, 9,    1, 8, 7],
                      [7, 0, 0,    0, 0, 8,    0, 0, 9]]

easy_test_board = [[6, 7, 2,    0, 3, 0,    9, 4, 0],
                   [8, 0, 0,    6, 0, 0,    0, 7, 5],
                   [0, 0, 9,    8, 2, 0,    6, 0, 0],

                   [1, 0, 0,    0, 0, 0,    0, 2, 0],
                   [0, 0, 0,    0, 0, 8,    7, 5, 0],
                   [2, 8, 4,    7, 5, 3,    1, 0, 9],

                   [7, 0, 3,    1, 8, 0,    0, 0, 0],
                   [4, 0, 5,    0, 0, 0,    3, 0, 0],
                   [0, 0, 0,    3, 7, 4,    0, 0, 6]]

notes = board_to_notes(another_test_board)
n_copy = copy_notes(notes)
easyness = (30, 2, 10)
# board = gen_board_level(easyness)
# print(board_to_str(board))
# print(infer_h(notes, 14))
# print(board_to_str(notes_to_board(notes)) + '\n\n')
# print('\nsolve_like_human output: ' + str(solve_like_human(notes, 5, 2, 0)) + '\n')
# print('notes:\n' + board_to_str(notes_to_board(notes)))
# print('notes copy:\n' + notes_to_str(n_copy))
# print('true: ' + str(notes == n_copy))

# for r in range(start[0], 9):
#   for c in range(start[1], 9):
#       print((r, c))
# things to test:
#   - copy board (check)
#   - infer
#   -  



# solve_like_human(notes, 100, 3, 10)
# print(notes is None)
# print(notes_to_str(notes))

# print('another test board:\n' + board_to_str(another_test_board))
# print('another test board notes:\n' + notes_to_str(notes))
# print('another test board notes to board:\n' + board_to_str(notes_to_board(notes)))

# print('before: ' + str(notes[(1, 6)]))
# first_inference_section(notes, ((0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)))
# print('after: '  + str(notes[(1, 6)]))

# print('before:\n' + board_to_str(another_test_board))
# first_inference(notes)
# new_board = notes_to_board(notes)
# print('after:\n' + board_to_str(new_board))

# print(board_to_str(notes_to_board(notes)))

# notes = board_to_notes(empty_board())
# print('before: ' + str(notes[(0, 0)]))
# annotate_list((0, 0), [1, 2, 3], notes)
# print('annotated to eliminate [1, 2, 3] from (0, 0): ' + str(notes[0, 0]))
# print('board:\n' + board_to_str(test_board))
# print('solved empty_test_board:\n' + board_to_str(solve(empty_board())))
# print('solved empty_test_board:\n' + str(solve(empty_board())))
# print('space_opts: ' + str(space_options_shuffled(empty_board(), 0, 0)))
# print('should just be a solved board \n' + board_to_str(rand_board()))
# solve(test_board)
# print(board_to_str(gen_board()))
# cProfile.run('solve(another_test_board)')
# print('starting')
# print('all but 1 hopefully: ' + str(space_options_shuffled(test_board, 1, 1)))
# print('row 0: ' + str(test_board[0]))
# print('possibilities: ' + str(possibilities))
# print('checking full (false): ' + str(full(test_board)))
# print('checking full (true): ' + str(full(full_test_board)))
# print(notes_to_str(board_to_notes(other_test_board)))
# print(init_notes(dict(), other_test_board))
# print('fillers random: ' + str(rand_fillers()))
def test_checks():
    board = copy_board(test_board)
    board[1][1] = 1
    print('row (true): ' +    str(check_row(board, 1)) + 
        '\ncol (false): ' +   str(check_col(board, 1)) +
        '\nbox (false): ' +   str(check_box(board, 0, 0)) +
        '\nspace (false): ' + str(check_space(board, 1, 1)))
def test_copy_board():
    test_board_copy = copy_board(test_board)
    test_board_copy[0][0] = 4
    print('hopefully just test_board:\n' + board_to_str(test_board))
    print('test_board_copy:\n' + board_to_str(test_board_copy))
# test_copy_board()
# test_checks()
# print(board_to_str(empty_board()))
# print(valid(other_test_board))
# print(rand_places())
# print(rand_fillers())
# print(gen_board())
# print(section_to_list(2, 2))
# print(all_sections())

def test_look_ahead():
    """
    >>> notes = board_to_notes(other_test_board)
    >>> solve_like_human(notes, 10, 2, 3)
    board solved
    True
    >>> print(board_to_str(notes_to_board(notes)))
    7 8 1   9 2 6   3 4 5
    4 3 9   8 5 1   7 2 6
    5 2 6   4 7 3   8 9 1
    <BLANKLINE>
    3 1 2   6 8 5   4 7 9
    9 5 8   7 3 4   1 6 2
    6 7 4   2 1 9   5 3 8
    <BLANKLINE>
    1 9 5   3 4 2   6 8 7
    2 4 7   5 6 8   9 1 3
    8 6 3   1 9 7   2 5 4
    <BLANKLINE>
    <BLANKLINE>
    """

testmod()
