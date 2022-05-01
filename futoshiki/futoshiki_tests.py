from doctest import *
from futoshiki_util import *
from futoshiki_checker import *
from futoshiki_solver import *
from futoshiki_generator import *
from futoshiki_human_solver import *

num_board_solved = \
    [[1, 2, 3, 4, 5],
     [2, 3, 4, 5, 1],
     [3, 4, 2, 1, 2],
     [4, 5, 1, 2, 3],
     [5, 1, 2, 3, 4]]

hor_ineq_board_solved = \
    [[  0,   0, '<', '<'],
     ['<', '<', '<', '>'],
     ['<', '<', '>', '<'],
     ['<', '>', '<', '<'],
     ['>', '<', '<', '<']]

ver_ineq_board_solved = \
    [['<', '<', '<', '<', '>'],
     ['<', '<', '<', '>', '<'],
     ['<',   0, '>', '<', '<'],
     ['<', '>', '<', '<', '<']]

board_solved = { board_type.NUM: num_board_solved, 
                 board_type.HOR_INEQ: hor_ineq_board_solved, 
                 board_type.VER_INEQ: ver_ineq_board_solved }

num_board_unsolved = [[0, 0, 0, 0, 5],
                      [0, 5, 0, 1, 0],
                      [0, 4, 5, 2, 0],
                      [1, 0, 3, 0, 4],
                      [0, 3, 0, 0, 2]]

hor_ineq_board_unsolved = [['>',   0,   0,   0],
                           [  0,   0,   0,   0],
                           ['<',   0,   0,   0],
                           [  0,   0,   0, '>'],
                           ['>', '>', '<', '>']]

ver_ineq_board_unsolved = [[  0,  0,  0,  0,  0],
                           [ '<', 0,  0,  0,  0],
                           [  0,  0,  0,  0,  0],
                           [  0,  0,  0, '>', 0]]

board_unsolved = { board_type.NUM: num_board_unsolved,
                   board_type.HOR_INEQ: hor_ineq_board_unsolved,
                   board_type.VER_INEQ: ver_ineq_board_unsolved }                       

num_board_mini = [[1, 0],
                  [0, 0]]

hor_ineq_board_mini = [[0], 
                       [0]]

ver_ineq_board_mini = [[0, 0]]

board_mini = { board_type.NUM: num_board_mini,
               board_type.HOR_INEQ: hor_ineq_board_mini,
               board_type.VER_INEQ: ver_ineq_board_mini }

num_board_inf_tests = [[0, 0, 0, 0,],
                       [0, 0, 0, 0,],
                       [0, 0, 0, 0,],
                       [0, 0, 0, 0,]]

hor_ineq_board_inf_tests = [['>',   0, '<'],
                            [  0,   0,   0],
                            [  0,   0, '>'],
                            ['<', '<', '<']]

ver_ineq_board_inf_tests = [[  0,   0,   0,   0],
                            [  0, '<',   0,   0],
                            [  0,   0,   0,   0]]

board_inf_tests = { board_type.NUM: num_board_inf_tests,
                    board_type.HOR_INEQ: hor_ineq_board_inf_tests,
                    board_type.VER_INEQ: ver_ineq_board_inf_tests }

num_board_hard_big = [[3, 0, 0, 2, 7, 0, 0],
                  [0, 0, 0, 5, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 3, 0, 0],
                  [6, 0, 0, 3, 0, 0, 4]]

hor_ineq_board_hard_big = [[  0,   0, '>',   0,   0,   0],
                       [  0,   0, '<',   0,   0, '>'],
                       [  0,   0,   0,   0, '>',   0],
                       [  0,   0,   0,   0,   0,   0],
                       [  0, '<',   0, '<',   0,   0],
                       [  0, '>',   0,   0,   0,   0],
                       [  0,   0, '<',   0,   0,   0]]

ver_ineq_board_hard_big = [[  0,   0,   0,   0,   0,   0,   0],
                       ['<',   0,   0,   0,   0,   0,   0],
                       [  0,   0, '>',   0,   0,   0,   0],
                       [  0, '<', '>',   0,   0,   0,   0],
                       [  0,   0,   0,   0,   0,   0,   0],
                       [  0,   0,   0, '<', '>',   0,   0]]

board_hard_big = { board_type.NUM: num_board_hard_big,
               board_type.HOR_INEQ: hor_ineq_board_hard_big,
               board_type.VER_INEQ: ver_ineq_board_hard_big }

num_board_hard = [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]

hor_ineq_board_hard = [['>',   0,   0,   0],
                       [  0,   0, '<',   0],
                       ['>',   0,   0,   0],
                       [  0,   0,   0, '>'],
                       ['>', '<',   0, '>']]

ver_ineq_board_hard = [[  0,   0, '>',   0,   0],
                       [  0,   0, '>', '<',   0],
                       [  0,   0, '<',   0,   0],
                       [  0,   0,   0,   0, '<'],]

board_hard = { board_type.NUM: num_board_hard,
               board_type.HOR_INEQ: hor_ineq_board_hard,
               board_type.VER_INEQ: ver_ineq_board_hard }

def test_futoshiki_checker():
    """
    >>> check_section_repitition(board_solved, (0, False))
    True
    >>> check_repitition(board_solved)
    False
    >>> check_row_hor_inequalities(board_solved, 3)
    True
    >>> check_hor_inequalities(board_solved)
    False
    >>> check_col_ver_inequalities(board_solved, 2)
    False
    >>> check_ver_inequalities(board_solved)
    False
    >>> check_board(board_solved)
    False
    >>> check_space(board_solved, 0, 0)
    True
    >>> check_space(board_solved, 2, 2)
    False
    >>> space_options(board_unsolved, 0, 0)
    [2, 3, 4]
    >>> check_space(board_mini, 0, 1)
    True
    """

def check_futoshiki_solver():
    """
    >>> def f(board):
    ...     solved = solve(board)
    ...     print(board_to_str(solved))
    >>> f(board_unsolved)
    4 > 1   2   3   5
    <BLANKLINE>
    2   5   4   1   3
    <                
    3 < 4   5   2   1
    <BLANKLINE>
    1   2   3   5 > 4
                >    
    5 > 3 > 1 < 4 > 2
    >>> valid(board_unsolved)
    True
    >>> valid(board_solved)
    True
    >>> valid(empty_board(4))
    False
    """

def test_futoshiki_generator():
    """ 
    >>> print(board_to_str(empty_board(5)))
    -   -   -   -   -
    <BLANKLINE>
    -   -   -   -   -
    <BLANKLINE>
    -   -   -   -   -
    <BLANKLINE>
    -   -   -   -   -
    <BLANKLINE>
    -   -   -   -   -
    """
    rrr = gen_board_graded(4, difficulty.HARD)

def test_futoshiki_human_solver():
    # notes infrastructure
    """
    NOTE: notes infrastructure
    >>> relationships(board_unsolved, 4, 3)
    {'<': ((3, 3),), '>': ((4, 2), (4, 4))}
    >>> board_to_notes(board_mini)
    {(0, 0): ([1], {'<': (), '>': ()}), (0, 1): ([2], {'<': (), '>': ()}), (1, 0): ([2], {'<': (), '>': ()}), (1, 1): ([1, 2], {'<': (), '>': ()})}
    >>> fill_in_ineqs(board_mini)
    >>> board_mini_notes = board_to_notes(board_mini)
    >>> board_mini_notes
    {(0, 0): ([1], {'<': (), '>': ()}), (0, 1): ([2], {'<': (), '>': ()}), (1, 0): ([2], {'<': (), '>': ()}), (1, 1): ([1, 2], {'<': (), '>': ()})}
    >>> highest_option(board_mini_notes, (1, 1))
    2
    >>> lowest_option(board_mini_notes, (1, 1))
    1
    >>> n_copy = copy_notes(board_mini_notes)
    >>> n_copy == board_mini_notes
    True
    >>> annotate(n_copy, (1, 1), 2)
    >>> n_copy == board_mini_notes
    False

    NOTE: inferences
    >>> third_inference(board_mini_notes)
    >>> new_mini_board = notes_to_num_board(board_mini_notes)
    >>> print(grid_list_to_str(new_mini_board))
    1 2
    2 1
    >>> inf_tests_notes = board_to_notes(board_inf_tests)
    >>> inf_tests_copy = copy_notes(inf_tests_notes)
    >>> def print_inf_tests():
    ...     print(grid_list_to_str(notes_to_num_board(inf_tests_copy)))
    >>> print('before:')
    before:
    >>> print_inf_tests()
    0 0 0 0
    0 0 0 0
    0 0 0 0
    0 0 0 0
    >>> infer(inf_tests_copy, 2)
    0
    >>> print('after:')
    after:
    >>> print_inf_tests()
    4 0 1 2
    2 0 4 3
    3 4 2 1
    1 2 3 4
    >>> bu_notes = board_to_notes(board_unsolved)
    >>> def print_notes_nums(notes):
    ...     print(grid_list_to_str(notes_to_num_board(notes)))
    >>> infer(bu_notes, 1)
    0
    >>> board_unsolved_cp = copy_board(board_unsolved)
    >>> board_unsolved_cp[board_type.NUM] = notes_to_num_board(bu_notes)
    >>> print(board_to_str(board_unsolved_cp))
    4 > 1   2   3   5
    <BLANKLINE>
    2   5   4   1   3
    <                
    3 < 4   5   2   1
    <BLANKLINE>
    1   2   3   5 > 4
                >    
    5 > 3 > 1 < 4 > 2
    >>> hard_notes = board_to_notes(board_hard_big)
    >>> infer(hard_notes, 10)
    3
    >>> print_notes_nums(hard_notes)
    3 0 0 2 7 0 0
    0 0 0 5 0 0 0
    0 0 7 6 0 0 0
    0 0 0 7 0 0 0
    7 0 0 4 0 0 0
    4 0 0 1 3 0 7
    6 0 0 3 0 0 4
    >>> hard_notes55 = board_to_notes(board_hard)
    >>> diff = (30, 5, 30)
    >>> solve_like_human(hard_notes55, diff)
    False
    >>> print(grid_list_to_str(notes_to_num_board(hard_notes55)))
    0 0 0 1 0
    1 0 2 3 0
    0 0 1 0 0
    0 0 0 2 1
    2 1 0 0 0
    """

# solve_like_human(board_to_notes(board_hard), 30, 5, 10)

def test_futoshiki_util():
    """
    >>> gen_options(5)
    [1, 2, 3, 4, 5]
    >>> section_to_list((False, 0), 4)
    [(0, 0), (1, 0), (2, 0), (3, 0)]
    >>> all_sections(5)
    [(0, False), (1, False), (2, False), (3, False), (4, False), (False, 0), (False, 1), (False, 2), (False, 3), (False, 4)]
    >>> l = [[1, 2, 3], [2, 3, 4]]
    >>> l2 = copy_2d_list(l)
    >>> l2[0][1] = 5
    >>> (l, l2)
    ([[1, 2, 3], [2, 3, 4]], [[1, 5, 3], [2, 3, 4]])
    >>> copy = copy_board(board_solved)
    >>> copy == board_solved
    True
    >>> copy[board_type.NUM][0] = 0
    >>> copy == board_solved
    False
    >>> full(board_solved)
    True
    >>> c2 = copy_board(board_solved)
    >>> c2 == board_solved
    True
    >>> fill_in_ineqs(c2)
    >>> c2 == board_solved
    False
    >>> tog_to_sep_index(30, 5)
    (<board_type.HOR_INEQ: 1>, 1, 1)
    >>> board_len(board_unsolved)
    5
    >>> print(board_to_str(board_hard_big))
    3   -   - > 2   7   -   -
    <BLANKLINE>
    -   -   - < 5   -   - > -
    <                        
    -   -   -   -   - > -   -
            >                
    -   -   -   -   -   -   -
        <   >                
    -   - < -   - < -   -   -
    <BLANKLINE>
    4   - > -   -   3   -   -
                <   >        
    6   -   - < 3   -   -   4
    >>> opp_ineq('>')
    '<'
    >>> opp_ineq('<')
    '>'
    >>> list_range(min=1, max=6)
    [1, 2, 3, 4, 5]
    >>> num_board_index_to_pos(15, 5)
    (3, 0)
    """

testmod()

def print_tests():
    # rand = rand_full_board(5)
    # print(board_to_str(gen_board_generic(4)))
    # print(board_to_str(rand)) # seems to work
    r = gen_board_graded(5, difficulty.EASY)
    print('easy:\n' + board_to_str(r))
    rr = gen_board_graded(5, difficulty.MEDIUM)
    print('medium:\n' + board_to_str(rr))
    rrr = gen_board_graded(5, difficulty.HARD)
    print('hard:\n' + board_to_str(rrr))
    rrrr = gen_board_graded(10, difficulty.WICKED)
    print('wicked:\n' + board_to_str(rrrr))

# print_tests()

# def valid_check(board):
#     sol_1 = solve(board)
#     for i in range(10):
#         next_sol = solve(board)
#         if not next_sol == sol_1:
#             return False
#     return True