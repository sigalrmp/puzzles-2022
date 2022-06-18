import cProfile
from doctest import *
from hashi_board import *
from hashi_util import *
from hashi_checker import *
from hashi_solver import *
from hashi_generator import *
from hashi_test_boards import *

board = {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {(2, 0): 2, (0, 2): 2}}, (0, 2): {'rem': 3, 'bridges': {}, 'poss': {(8, 2): 2, (0, 4): 2, (0, 0): 2}}, (0, 4): {'rem': 3, 'bridges': {}, 'poss': {(3, 4): 2, (0, 2): 2}}, (1, 1): {'rem': 3, 'bridges': {}, 'poss': {(3, 1): 2, (1, 3): 2}}, (1, 3): {'rem': 1, 'bridges': {}, 'poss': {(5, 3): 2, (1, 1): 2}}, (2, 0): {'rem': 3, 'bridges': {}, 'poss': {(4, 0): 2, (0, 0): 2, (2, 5): 2}}, (2, 5): {'rem': 1, 'bridges': {}, 'poss': {(4, 5): 2, (2, 0): 2}}, (3, 1): {'rem': 4, 'bridges': {}, 'poss': {(7, 1): 2, (1, 1): 2, (3, 4): 2}}, (3, 4): {'rem': 5, 'bridges': {}, 'poss': {(6, 4): 2, (0, 4): 2, (3, 1): 2}}, (4, 0): {'rem': 3, 'bridges': {}, 'poss': {(6, 0): 2, (2, 0): 2, (4, 5): 2}}, (4, 5): {'rem': 2, 'bridges': {}, 'poss': {(7, 5): 2, (2, 5): 2, (4, 0): 2}}, (5, 3): {'rem': 1, 'bridges': {}, 'poss': {(7, 3): 2, (1, 3): 2}}, (6, 0): {'rem': 3, 'bridges': {}, 'poss': {(8, 0): 2, (4, 0): 2, (6, 4): 2}}, (6, 4): {'rem': 2, 'bridges': {}, 'poss': {(8, 4): 2, (3, 4): 2, (6, 0): 2}}, (7, 1): {'rem': 3, 'bridges': {}, 'poss': {(3, 1): 2, (7, 3): 2}}, (7, 3): {'rem': 4, 'bridges': {}, 'poss': {(5, 3): 2, (7, 5): 2, (7, 1): 2}}, (7, 5): {'rem': 2, 'bridges': {}, 'poss': {(4, 5): 2, (7, 3): 2}}, (8, 0): {'rem': 3, 'bridges': {}, 'poss': {(6, 0): 2, (8, 2): 2}}, (8, 2): {'rem': 2, 'bridges': {}, 'poss': {(0, 2): 2, (8, 4): 2, (8, 0): 2}}, (8, 4): {'rem': 1, 'bridges': {}, 'poss': {(6, 4): 2, (8, 2): 2}}}
board_grid = [[3, 0, 3, 0, 3, 0],
              [0, 3, 0, 1, 0, 0],
              [3, 0, 0, 0, 0, 1],
              [0, 4, 0, 0, 5, 0],
              [3, 0, 0, 0, 0, 2],
              [0, 0, 0, 1, 0, 0],
              [3, 0, 0, 0, 2, 0],
              [0, 3, 0, 4, 0, 2],
              [3, 0, 2, 0, 1, 0]]

zero_board_grid = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]

mini_board_grid = [[2, 0, 1],
                   [1, 0, 0]]

hard_board_grid = [[3, 0, 3, 0, 2, 0, 0, 3, 0],
                   [0, 1, 0, 0, 0, 0, 2, 0, 2],
                   [3, 0, 0, 2, 0, 2, 0, 2, 0],
                   [0, 2, 0, 0, 3, 0, 3, 0, 5],
                   [4, 0, 0, 4, 0, 3, 0, 3, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 3],
                   [3, 0, 1, 0, 3, 0, 1, 0, 0],
                   [0, 2, 0, 3, 0, 2, 0, 3, 0],
                   [2, 0, 2, 0, 4, 0, 0, 0, 0],
                   [0, 4, 0, 2, 0, 1, 0, 0, 3],
                   [3, 0, 2, 0, 3, 0, 0, 2, 0],
                   [0, 2, 0, 1, 0, 0, 0, 0, 0],
                   [2, 0, 4, 0, 4, 0, 2, 0, 2]]

# {(x, y): {'rem': remaining_cons, 'poss: {(x, y): remaining_cons_(0 to 2)}}}

def test_hashi_board():
    """
    >>> coord((2, 3), 'y')
    3
    >>> other_axis('x')
    'y'
    >>> next_node((2, 3), 'x', 1)
    (3, 3)
    >>> grid_to_board(board_grid) == board
    True
    >>> dir_of_bridge('x', 1, (3, 1), (3, 4), (5, 3))
    True
    >>> dir_of_bridge('x', 1, (3, 4), (3, 1), (5, 5))
    False
    >>> dir_of_bridge('x', -1, (3, 4), (3, 1), (1, 3))
    True
    >>> dir_of_bridge('y', -1, (3, 4), (8, 4), (5, 6))
    False
    >>> overlapping((0, 0), (0, 4), (1, 1), (1, 3))
    False
    >>> overlapping((3, 1), (3, 4), (1, 3), (5, 3))
    True
    >>> bridge(board, (0, 0), (0, 2))
    >>> board[(0, 0)]['poss'][(0, 2)]
    1
    >>> board[(0, 0)]['rem']
    2
    >>> board[(0, 2)]['poss'][(0, 0)]
    1
    >>> board[(0, 2)]['rem']
    2
    >>> rem_poss(changed_obj(grid_to_board(mini_board_grid), basic_inference), (0, 0))
    2
    >>> relative_node((2, 0), ('x', 1), 8)
    (10, 0)
    """

def test_hashi_checker():
    """
    >>> zero_board = grid_to_board(zero_board_grid)
    >>> full(zero_board)
    True
    >>> full(board)
    False
    >>> connected(board)
    False
    >>> mini_board = grid_to_board(mini_board_grid)
    >>> print(dict_to_str(mini_board))
    (0, 0): {'rem': 2, 'bridges': {}, 'poss': {(1, 0): 2, (0, 2): 2}}
    (0, 2): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    (1, 0): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    <BLANKLINE>
    >>> bridge(mini_board, (0, 0), (1, 0))
    >>> bridge(mini_board, (0, 0), (0, 2))
    >>> print(dict_to_str(mini_board))
    (0, 0): {'rem': 0, 'bridges': {(1, 0): 1, (0, 2): 1}, 'poss': {(1, 0): 1, (0, 2): 1}}
    (0, 2): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 1}}
    (1, 0): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 1}}
    <BLANKLINE>
    >>> full(mini_board)
    True
    >>> connected(mini_board)
    True
    >>> solved(mini_board)
    True
    >>> bridge_points((0, 0), (3, 0))
    [(1, 0), (2, 0)]
    >>> bridge_points((3, 8), (3, 2))
    [(3, 7), (3, 6), (3, 5), (3, 4), (3, 3)]
    """

def test_hashi_solver():
    """
    >>> mini_board = grid_to_board(mini_board_grid)
    >>> print(dict_to_str(mini_board))
    (0, 0): {'rem': 2, 'bridges': {}, 'poss': {(1, 0): 2, (0, 2): 2}}
    (0, 2): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    (1, 0): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    <BLANKLINE>
    >>> def print_sols(b, n):
    ...     sols = find_node_sols(b, n)
    ...     for s in sols:
    ...         print(str(n) + ': ' + str(s[n]))
    >>> print_sols(mini_board, (0, 0))
    (0, 0): {'rem': 0, 'bridges': {(1, 0): 1, (0, 2): 1}, 'poss': {(1, 0): 0, (0, 2): 0}}
    >>> print_sols(board, (0, 0))
    (0, 0): {'rem': 0, 'bridges': {(0, 2): 2, (2, 0): 1}, 'poss': {(2, 0): 0, (0, 2): 0}}
    (0, 0): {'rem': 0, 'bridges': {(0, 2): 1, (2, 0): 2}, 'poss': {(2, 0): 0, (0, 2): 0}}
    >>> print_sols(board, (1, 1))
    (1, 1): {'rem': 0, 'bridges': {(3, 1): 2, (1, 3): 1}, 'poss': {(3, 1): 0, (1, 3): 0}}
    >>> basic_inference(mini_board)
    >>> print(dict_to_str(mini_board))
    (0, 0): {'rem': 2, 'bridges': {}, 'poss': {(1, 0): 1, (0, 2): 1}}
    (0, 2): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 1}}
    (1, 0): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 1}}
    <BLANKLINE>
    >>> mini_board_2 = grid_to_board(mini_board_grid)
    >>> infer(mini_board_2, 1, 10)
    0
    >>> solved(mini_board_2)
    True
    >>> print(dict_to_str(mini_board_2))
    (0, 0): {'rem': 0, 'bridges': {(1, 0): 1, (0, 2): 1}, 'poss': {(1, 0): 0, (0, 2): 0}}
    (0, 2): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 0}}
    (1, 0): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 0}}
    <BLANKLINE>
    >>> board_2 = grid_to_board(board_grid)
    >>> bridge_similarities({(0, 2): 3, (9, 2): 1}, {(0, 0): 7, (0, 2): 2, (9, 2): 0})
    {(0, 2): 2, (9, 2): 0}
    >>> poss_similarities({(0, 2): 3, (9, 2): 1}, {(0, 0): 7, (0, 2): 2, (9, 2): 0})
    {(0, 2): 3, (9, 2): 1}
    >>> differences({(1, 2): 3, (3, 2): 4}, {(3, 4): 2, (3, 2): 1})
    {(1, 2): 3, (3, 2): 4}
    >>> b = grid_to_board(board_grid)
    >>> sols_first_node = find_node_sols(b, (0, 0))
    >>> print_sols(b, (0, 0))
    (0, 0): {'rem': 0, 'bridges': {(2, 0): 1, (0, 2): 2}, 'poss': {(2, 0): 0, (0, 2): 0}}
    (0, 0): {'rem': 0, 'bridges': {(2, 0): 2, (0, 2): 1}, 'poss': {(2, 0): 0, (0, 2): 0}}
    >>> execute_common_changes(b, sols_first_node)
    >>> b[(0, 0)]
    {'rem': 1, 'bridges': {(2, 0): 1, (0, 2): 1}, 'poss': {(2, 0): 1, (0, 2): 1}}
    >>> infer(board_2, 10, 10)
    8
    >>> solved(board_2)
    True
    >>> board_3 = grid_to_board(board_grid)
    >>> look_ahead(board_3, difficulty.EASY, 0)
    >>> solve(board_3, difficulty.EASY)
    True
    >>> board_3 == board
    False
    """

def test_hashi_generator():
    """
    >>> b = copy_board(board)
    >>> board_ready(b, difficulty.EASY)
    False
    """

def test_hashi_util():
    """
    >>> d = {0: {'a': 0, 'b': 1}, 1: {'c': 2, 'd': 3}}
    >>> d_copy = copy_2d_dict(d)
    >>> d == d_copy
    True
    >>> d[0]['a'] = 4
    >>> d == d_copy
    False
    """

testmod()