from random import randrange
from hashi_solver import *
from hashi_board import *
from hashi_checker import *
from hashi_util import *
from doctest import *

def pick_node(nodes, dims):
    if len(nodes) == 0:
        return (randrange(0, dims['x']), randrange(0, dims['y']))
    else:
        return pick_weighted(nodes)

def test_pick_node():
    """
    >>> pick_node([[(2, 3), 1], [(4, 2), 0]], {'x': 3, 'y': 4})
    (2, 3)
    """

def add_node_to_nodes(nodes, new_node, degrading_factor=0):
    if len(nodes) == 1: nodes += [[new_node, 1]]
    else: add_option_to_weighted_list(nodes, new_node, degrading_factor)

def maintain_nodes(nodes, board, cap):
    for i in range_len(nodes):
        n = nodes[i]
        if board[n[0]]['rem'] >= cap:
            n[1] = 0.00000001

def test_add_node_to_nodes():
    """
    >>> nodes = [[(0, 0), 1]]
    >>> add_node_to_nodes(nodes, (4, 0), 0.5)
    >>> nodes
    [[(0, 0), 1], [(4, 0), 1]]
    >>> add_node_to_nodes(nodes, (2, 3), 0.5)
    >>> nodes
    [[(0, 0), 0.5], [(4, 0), 0.5], [(2, 3), 1]]
    """

def add_node_to_board(board, new_node):
    board[new_node] = {'rem': 8, 'bridges': {}, 'poss': {}}

def test_add_node_to_board():
    """
    >>> board = {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {}}}
    >>> add_node_to_board(board, (2, 3))
    >>> board
    {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {}}, (2, 3): {'rem': 8, 'bridges': {}, 'poss': {}}}
    """

def add_node(board, nodes, bridged_node, new_node, count, degrading_factor):
    if len(nodes) == 0:
        add_node_to_board(board, bridged_node)
        add_node_to_nodes(nodes, bridged_node)
    add_node_to_board(board, new_node)
    fill_poss_cons(board)
    for n1 in board:
        for n2 in board[n1]['bridges']:
            remove_overlapping_from_poss(board, n1, n2)
    for i in range(count):
        if can_be_bridged(board, bridged_node, new_node):
            bridge(board, bridged_node, new_node)
            if i == 0: add_node_to_nodes(nodes, new_node, degrading_factor)
        else: return False

def test_add_node():
    """
    >>> board = {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {}}}
    >>> nodes = [[(0, 0), 1]]
    >>> add_node(board, nodes, (0, 0), (0, 3), 1, 0.5)
    >>> nodes
    [[(0, 0), 1], [(0, 3), 1]]
    >>> board
    {(0, 0): {'rem': 2, 'bridges': {(0, 3): 1}, 'poss': {(0, 3): 1}}, (0, 3): {'rem': 7, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 1}}}
    """

def can_be_bridged(board, n1, n2):
    a = n1 in board[n2]['poss'] and board[n2]['poss'][n1] > 0
    b = n2 in board[n1]['poss'] and board[n1]['poss'][n2] > 0
    c = board[n1]['rem'] > 0 and board[n2]['rem'] > 0
    d = True
    for n in board[n1]['bridges']:
        d &= not n2 in bridge_points(n1, n)
    for n in board[n2]['bridges']:
        d &= not n1 in bridge_points(n2, n)
    for n in board:
        if not n == n1 and not n == n2:
            d &= not n in bridge_points(n1, n2)
    return a and b and c and d

def test_can_be_bridged():
    """
    >>> board = {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {}}, (2, 3): {'rem': 8, 'bridges': {}, 'poss': {}}}
    >>> can_be_bridged(board, (0, 0), (2, 3))
    False
    >>> board = {(0, 0): {'rem': 0, 'bridges': {}, 'poss': {}}, (0, 3): {'rem': 8, 'bridges': {}, 'poss': {}}}
    >>> fill_poss_cons(board)
    >>> can_be_bridged(board, (0, 0), (0, 3))
    False
    >>> board = {(0, 0): {'rem': 3, 'bridges': {}, 'poss': {}}, (0, 2): {'rem': 8, 'bridges': {}, 'poss': {}}, (0, 3): {'rem': 8, 'bridges': {}, 'poss': {}}}
    >>> fill_poss_cons(board)
    >>> can_be_bridged(board, (0, 0), (0, 3))
    False
    """

def pick_dir():
    axis = randrange(0, 2)
    axis = 'x' if axis == 0 else 'y'
    dir = 2 * randrange(0, 2) - 1
    return (axis, dir)

# pick_dir is tested and seems to work

def pick_dist(node, dir, dims, degrading_factor):
    lengths = list(range(coord(node, dir[0]) - 1)) if dir[1] < 0 else \
              list(range(dims[dir[0]] - coord(node, dir[0])))
    for i in range_len(lengths):
        lengths[i] = (lengths[i] + 1, degrading_factor ** lengths[i]) if not i == 0 else (lengths[i] + 1, 0.0001)
    return pick_weighted(lengths) # NOTE this sometimes returns none so that should be taken into account and dealt with

# pick_dist is tested and seems to work, but see the NOTE above

def pick_bridge_count():
    return 1 if random() < 2/3 else 2

# pick_bridge_count is tested and seems to work

def fix_rem_count(board):
    for n in board:
        cons = 0
        for n2 in board[n]['bridges']:
            cons += board[n]['bridges'][n2]
        board[n]['rem'] = cons

def test_fix_rem_count():
    """
    >>> b = {(4, 0): {'rem': 6, 'bridges': {(3, 0): 1, (5, 0): 1}, 'poss': {(5, 0): 2, (3, 0): 2}}, (3, 0): {'rem': 7, 'bridges': {(4, 0): 1}, 'poss': {(4, 0): 2}}, (5, 0): {'rem': 6, 'bridges': {(4, 0): 1, (5, 2): 1}, 'poss': {(4, 0): 2, (5, 2): 1}}, (5, 2): {'rem': 7, 'bridges': {(5, 0): 1}, 'poss': {(5, 0): 1}}}
    >>> fix_rem_count(b)
    >>> print(dict_to_str(b))
    (4, 0): {'rem': 2, 'bridges': {(3, 0): 1, (5, 0): 1}, 'poss': {(5, 0): 2, (3, 0): 2}}
    (3, 0): {'rem': 1, 'bridges': {(4, 0): 1}, 'poss': {(4, 0): 2}}
    (5, 0): {'rem': 2, 'bridges': {(4, 0): 1, (5, 2): 1}, 'poss': {(4, 0): 2, (5, 2): 1}}
    (5, 2): {'rem': 1, 'bridges': {(5, 0): 1}, 'poss': {(5, 0): 1}}
    <BLANKLINE>
    """

def refresh_bridges(board):
    for n in board: 
        board[n]['bridges'] = {}
 
def board_ready(board, diff):
    # print('board:\n' + dict_to_str(board))
    board_copy = copy_board(board)
    refresh_board(board_copy)
    # print('refreshed board copy:\n' + dict_to_str(board_copy))
    solvable = solve(board_copy, diff)
    # print('solvable: ' + str(solvable) + '; board after solving:\n' + dict_to_str(board_copy))
    refresh_board(board_copy)
    # print('re-refreshed board:\n' + dict_to_str(board_copy))
    hard_enough_solve = solve(board_copy, diff.value['hard_enough_pars'])
    # print('solvable by hard_enough.EASY: ' + str(hard_enough_solve) + 
    #       '; board after solving by hard_enough.EASY:\n' + dict_to_str(board_copy))
    hard_enough = not hard_enough_solve
    return solvable and hard_enough

# board_ready has been lightly tested, and seems to be working

def all_poss_spaces_full(board, dims):
    full = True
    for x in range(dims['x']):
        for y in range(dims['y']):
            full &= (x, y) in board
    return full

def gen_board_h(last_board, last_nodes, dist_degrading_factor, node_degrading_factor, diff, dims, failed_count):
    if failed_count > min(50, 4 * (dims['x'] + dims['y'])): return False
    if len(last_nodes) >= dims['x'] * dims['y'] / 2.6:
        print('too many filled; board:\n\n' + dict_to_str(last_board) + '\n\n'); return False
    # if len(last_nodes) >= 10: return changed_obj(last_board, refresh_board)
    board = copy_board(last_board)
    nodes = copy_2d_list(last_nodes)
    maintain_nodes(nodes, board, 5)
    node = pick_node(nodes, dims)
    dir = pick_dir()
    dist = pick_dist(node, dir, dims, dist_degrading_factor)
    count = pick_bridge_count()
    failed = dist is None
    if not failed:
        new_node = relative_node(node, dir, dist)
        failed = new_node in board or (add_node(board, nodes, node, new_node, count, node_degrading_factor) is False)
    ready = len(board) > 0 and board_ready(board, diff)
    impossible = not closed_check(board)
    if failed or impossible or (len(board) > 8 and not solve(board, diff)): 
        return gen_board_h(last_board, last_nodes, dist_degrading_factor, node_degrading_factor, diff, dims, failed_count + 1)
    if ready: return changed_obj(board, refresh_board)
    new_board = gen_board_h(board, nodes, dist_degrading_factor, node_degrading_factor, diff, dims, 0)
    if new_board is False:
        return gen_board_h(last_board, last_nodes, dist_degrading_factor, node_degrading_factor, diff, dims, failed_count + 1)
    else: return new_board

def refresh_board(board):
    fix_rem_count(board)
    refresh_bridges(board)
    fill_poss_cons(board)



    # >>> print(dict_to_str(b))
    # """
    # >>> too_full = {(0, 5): {'rem': 4, 'bridges': {(0, 4): 1, (0, 6): 1, (6, 5): 2}, 'poss': {(6, 5): 2, (0, 6): 2, (0, 4): 2}}, (0, 4): {'rem': 6, 'bridges': {(0, 5): 1, (0, 3): 1}, 'poss': {(6, 4): 2, (0, 5): 2, (0, 3): 2}}, (0, 2): {'rem': 8, 'bridges': {}, 'poss': {(4, 2): 2, (0, 3): 2}}, (0, 6): {'rem': 7, 'bridges': {(0, 5): 1}, 'poss': {(6, 6): 2, (0, 5): 2}}, (0, 3): {'rem': 6, 'bridges': {(0, 4): 1, (4, 3): 1}, 'poss': {(4, 3): 2, (0, 4): 2, (0, 2): 2}}, (4, 3): {'rem': 6, 'bridges': {(0, 3): 1, (4, 1): 1}, 'poss': {(0, 3): 2, (4, 2): 2}}, (6, 5): {'rem': 3, 'bridges': {(0, 5): 2, (6, 6): 1, (6, 4): 2}, 'poss': {(0, 5): 2, (6, 6): 2, (6, 4): 0}}, (6, 6): {'rem': 7, 'bridges': {(6, 5): 1}, 'poss': {(0, 6): 2, (6, 5): 2}}, (4, 1): {'rem': 7, 'bridges': {(4, 3): 1}, 'poss': {(4, 2): 2}}, (4, 2): {'rem': 8, 'bridges': {}, 'poss': {(0, 2): 2, (4, 3): 2, (4, 1): 2}}, (6, 4): {'rem': 6, 'bridges': {(6, 5): 2}, 'poss': {(0, 4): 2, (6, 5): 0}}}
    # >>> cb = copy_board(b)
    # >>> board_ready(cb, difficulty.EASY)
    # >>> solve(cb, difficulty.EASY)
    # >>> solve(cb, hard_enough.EASY)
    # >>> print(dict_to_str(cb))
    # >>> cb
    # >>> def board_to_grid(board, dims):
    # ...     l = []
    # ...     for r in range(dims['x']):
    # ...         row = []
    # ...         for c in range(dims['y']):
    # ...             if (r, c) in board:
    # ...                 row += [board[(r, c)]['rem']]
    # ...             else: row += [0]
    # ...         l += [row]
    # ...     return l
    # """

def enter(): return '\n'

# def test_gen_board_h():
#     """
#     >>> b = gen_board_h({}, [], dist_degrading_factor, node_degrading_factor, difficulty.HARD, {'x': 5, 'y': 5}, 0) 
#     >>> b
#     >>> if type(b) is dict: print(dict_to_str(b))
#     ... else: print('not a dict')
#     """
    # >>> bc = copy_board(b)
    # >>> print(dict_to_str(b))
    # >>> print('solvable on easy: ' + str(solve(b, difficulty.EASY)))
    # >>> print(dict_to_str(b))
    # >>> print('solvable on hard enough for easy: ' + str(solve(bc, hard_enough.EASY)))
    # >>> print(dict_to_str(bc))    
    # """


def gen_board(diff, dims={'x': 5, 'y': 5}):
    return gen_board_h({}, [], dist_degrading_factor, node_degrading_factor, diff, dims, 0)

testmod()