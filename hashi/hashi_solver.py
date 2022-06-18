from hashi_util import *
from hashi_board import *
from hashi_checker import *
from hashi_test_boards import *
from doctest import *

# strategies:
#   - for each node, try all possible configurations and execute whatever is constant throughout them
# super simple inference (done):
#   - for each possible connection for each node, if the remaining connections for either the node or the
#     possible connection is less than 2, the number for the connection should be set to that remainder
# finding all possibilities (done):
#   - for each node
#       - for each connection
#           - for each number between 0 and the max poss cons
#  

def basic_inference(board):
    for node in board:
      for con in board[node]['poss']:
          node_rem = board[node]['rem']
          con_rem = board[con]['rem']
          node_count = board[node]['poss'][con]
          con_count = board[con]['poss'][node]
          new_count = min(node_rem, con_rem, node_count, con_count)
          update_poss_count(board, node, con, new_count)

def check_node_sol(board, node):
    return closed_check(board) and \
           0 <= board[node]['rem'] <= rem_poss(board, node)

def closed_check(board):
    basic_inference(board)
    visited = [[]]
    def rec(node):
        if not node in visited[0]: visited[0] += [node]
        if len(visited[0]) < len(board):
            for neighbor in list(board[node]['bridges']) + list(board[node]['poss']):
                if not neighbor in visited[0] and (neighbor in board[node]['bridges'] or board[node]['poss'][neighbor] > 0):
                    rec(neighbor)
    if not len(board) == 0: rec(list(board)[0])
    return len(visited[0]) == len(board)

def find_node_sols(board, node):
    sols = [[]]
    def rec(rboard, con_i):
        cons = list(rboard[node]['poss']) # possible bridges for the node
        basic_inference(rboard)
        if rboard[node]['rem'] == 0: sols[0] += [rboard]
        elif not con_i >= len(cons):
            con = cons[con_i]
            for i in range(rboard[node]['poss'][con] + 1):
                new_board = copy_board(rboard)
                for j in range(i):
                    bridge(new_board, node, con)
                if check_node_sol(new_board, node):
                    rec(new_board, con_i + 1)
    rec(board, 0)
    # if len(sols[0]) == 0 and not board[node]['rem'] == 0:
    #     raise Exception('FLAGGGGGG')
    return sols[0]

def differences(d1, d2):
    diffs = {} 
    for n in d1: 
        if not n in d2 or not d1[n] == d2[n]:
            diffs[n] = d1[n]
    return diffs

def bridge_similarities(d1, d2):
    sims = {}
    for n in d1:
        if n in d2:
            sims[n] = min(d1[n], d2[n])
    return sims

def poss_similarities(d1, d2):
    sims = {}
    for n in d1:
        if n in d2:
            sims[n] = max(d1[n], d2[n]) 
    return sims

def execute_bridge_changes(board, node, bridge_changes):
    for n in bridge_changes:
        new_bridge_count = bridge_changes[n] if not n in board[node]['bridges'] else bridge_changes[n] - board[node]['bridges'][n] 
        for i in range(new_bridge_count):
            bridge(board, node, n)

# def test_execute_bridge_changes():
#     """
#     >>> board = grid_to_board(hard_board_grid)
#     >>> sols = find_node_sols(board, (12, 2))
#     >>> len(sols)
#     5
#     >>> for s in sols:
#     ...     print(dict_to_str(s))
#     ...     print('')
#     >>> bridge_changes = common_changes_node(board, sols, (12, 2))
#     >>> print(bridge_changes)
#     >>> execute_changes(board, (12, 2), bridge_changes)
#     >>> print(dict_to_str(board))
#     """

# def execute_poss_changes(board, node, poss_changes):
#     for n in poss_changes:
#         board[node]['poss'][n] = poss_changes[n]

def execute_changes(board, node, bridge_changes):
    execute_bridge_changes(board, node, bridge_changes)
    # execute_poss_changes(board, node, poss_changes) 


def common_changes_node(board, sols, node):
    basic_inference(board)
    bridge_changes = differences(sols[0][node]['bridges'], board[node]['bridges'])
    # poss_changes =   differences(sols[0][node]['poss'],    board[node]['poss'])
    for sol_i in range(1, len(sols)):
        sol = sols[sol_i]
        bridge_changes = bridge_similarities(bridge_changes, sol[node]['bridges'])
        # poss_changes = poss_similarities(poss_changes, sol[node]['poss'])
    # poss_changes = differences(poss_changes, board[node]['poss'])
    return bridge_changes

def execute_common_changes(board, sols):
    basic_inference(board)
    if len(sols) >= 1:
        for node in board:
            execute_changes(board, node, common_changes_node(board, sols, node))

def infer_node(board, node, max_sols_len):
    sols = find_node_sols(board, node)
    if len(sols) <= max_sols_len:
        execute_common_changes(board, sols)

def infer(board, i, max_sols_len):
    start_board = copy_board(board)
    for node in board:
        infer_node(board, node, max_sols_len)
    if i == 0 or board == start_board:
        return i
    else: return infer(board, i - 1, max_sols_len)

def look_ahead(board, diff, start_index):
    nodes = list(board)
    next_start_index = None
    sols = None
    for i in range(start_index, len(nodes)):
        n = nodes[i]
        n_sols = find_node_sols(board, n)
        if 1 < len(n_sols) < diff.value['max_look_ahead_sols']:
            if not i == len(nodes) - 1: sols = n_sols; next_start_index = i + 1
            break
    if not sols is None:
        look_ahead_h(board, diff, sols)
        return next_start_index
    
def look_ahead_h(board, diff, sols):
    for sol in sols:
        infer(sol, diff.value['max_look_ahead_depth'], diff.value['max_sols_len'])
    execute_common_changes(board, sols)

def solve(board, diff):
    def rec(i, start_la_index, count):
        if i == 0: return False
        else:
            new_i = infer(board, i, diff.value['max_sols_len'])
            if not start_la_index is None:
                new_start_la_index = look_ahead(board, diff, start_la_index)
            else: return solved(board)
            if solved(board): return True
            else: return rec(new_i, new_start_la_index, count + 1)
    return rec(diff.value['max_inference_depth'], 0, 0)

def test():
    """
    >>> mb = grid_to_board(mini_board_grid)
    >>> print(dict_to_str(mb))
    (0, 0): {'rem': 2, 'bridges': {}, 'poss': {(1, 0): 2, (0, 2): 2}}
    (0, 2): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    (1, 0): {'rem': 1, 'bridges': {}, 'poss': {(0, 0): 2}}
    <BLANKLINE>
    >>> solve(mb, difficulty.EASY)
    True
    >>> print(dict_to_str(mb))
    (0, 0): {'rem': 0, 'bridges': {(1, 0): 1, (0, 2): 1}, 'poss': {(1, 0): 0, (0, 2): 0}}
    (0, 2): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 0}}
    (1, 0): {'rem': 0, 'bridges': {(0, 0): 1}, 'poss': {(0, 0): 0}}
    <BLANKLINE>
    >>> hard_board = grid_to_board(hard_board_grid)
    >>> solve(hard_board, difficulty.EASY)
    >>> solve(hard_board, difficulty.MEDIUM)
    """
difficulty
testmod()