from doctest import *
from hashi_util import *
from hashi_test_boards import *
# board structure:
#   {(x, y): {'rem': remaining_cons, 'poss': {(x, y): remaining_cons_(0 to 2)}, 'bridges': {(x, y): #bridges}}}

def board_dims(board):
    max_x = 0
    max_y = 0
    for n in board:
        max_x = max(max_x, n[0])
        max_y = max(max_y, n[1])
    return {'x': max_x + 1, 'y': max_y + 1}

def first_node(board):
    min_x = 0
    min_y = 0
    for n in board:
        min_x = min(min_x, n[0])
        min_y = min(min_y, n[1])
    return (min_x, min_y)

def last_node(board):
    dims = board_dims(board)
    return (dims['x'] - 1, dims['y'] - 1)

def coord(node, coord):
    if coord == 'x':
        return node[0]
    if coord == 'y':
        return node[1]

def relative_node(n1, dir, dist):
    dir_dist = dist * dir[1]
    axis2 = other_axis(dir[0])
    new_node_d = {dir[0]: dir_dist + coord(n1, dir[0]),
                  axis2: coord(n1, axis2)}
    return (new_node_d['x'], new_node_d['y'])

def other_axis(axis):
    return 'x' if axis == 'y' else 'y'

def test_relative_node():
    """
    >>> relative_node((0, 0), ('x', 1), 4)
    (4, 0)
    >>> relative_node((2, 7), ('y', -1), 4)
    (2, 3)
    """

testmod()

def next_node(node, axis, dir):
    i = coord(node, axis) + dir
    if axis == 'x': return (i, coord(node, 'y'))
    elif axis == 'y': return (coord(node, 'x'), i)

def closest(board, node, axis, dir):
    dims = board_dims(board)
    def rec(n):
        next_n = next_node(n, axis, dir)
        if 0 <= coord(next_n, axis) < dims[axis]:
            if next_n in board: return next_n
            else: return rec(next_n)
    return rec(node)

def fill_poss_cons(board):
    for n in board:
        board[n]['poss'] = {}
        def fill_axis(axis):
            for d in [1, -1]:
                c = closest(board, n, axis, d)
                if not c is None: board[n]['poss'][c] = 2
        fill_axis('x'); fill_axis('y')

def dir_of_bridge(axis, dir, bn1, bn2, n):
    if dir == 0: return False
    axis2 = other_axis(axis)
    bn1_a  = coord(bn1, axis);  bn2_a  = coord(bn2, axis)
    bn1_a2 = coord(bn1, axis2); bn2_a2 = coord(bn2, axis2)
    return bn1_a == bn2_a \
      and coord(n, axis) * dir > bn1_a * dir \
      and min(bn1_a2, bn2_a2) < coord(n, axis2) < max(bn1_a2, bn2_a2)

def overlapping(bn1, bn2, n1, n2):
    ns = [n1, n2]
    # def check_axis(axis, whatever else):
    #   - check if n1 is on either side of bridge
    #       - if it is, return (n2 is on the other side)
    def check_axis(axis):
        def get_n1_dir():
            def rec(d):
                return d if dir_of_bridge(axis, d, bn1, bn2, n1) \
                    else rec(-d) if d > 0 else 0
            return rec(1)
        return dir_of_bridge(axis, -get_n1_dir(), bn1, bn2, n2)
    return check_axis('x') or check_axis('y')

def remove_poss(board, n1, n2, rec=True):
    dict.pop(board[n1]['poss'], n2)
    if rec: remove_poss(board, n2, n1, False)

def remove_poss_list(board, n1, n2_list):
    for n2 in n2_list:
        remove_poss(board, n1, n2)

def remove_overlapping_from_poss(board, n1, n2):
    for n1_ in board:
        to_remove = []
        for n2_ in board[n1_]['poss']:
            if overlapping(n1, n2, n1_, n2_):
                to_remove += [n2_]
        remove_poss_list(board, n1_, to_remove)

def bridge(board, n1, n2):
    def debug(f, s):
        try: board[f]['poss'][s]
        except: raise Exception('board[' + str(f) + '][poss][' + str(s) + '] did not work. board:\n' + dict_to_str(board))
        if board[f]['poss'][s] == 0:
            crash_data = str(f) + ' and ' + str(s) + ' are being bridged, but board says they cannot be. board[' + str(f) + '][poss][' + str(s) + '] == 0\nboard:\n' + dict_to_str(board)
            raise Exception(crash_data)
        if board[f]['rem'] == 0:
            crash_data = str(f) + ' and ' + str(s) + ' are being bridged, but ' + str(f) + ' has no more connections. board\n' + dict_to_str(board)
            raise Exception(crash_data)
    debug(n1, n2); debug(n2, n1)
    def br(f, s): 
        board[f]['poss'][s] -= 1; board[f]['rem'] -= 1
        if s in board[f]['bridges']: board[f]['bridges'][s] += 1
        else: board[f]['bridges'][s] = 1
    br(n1, n2); br(n2, n1)
    remove_overlapping_from_poss(board, n1, n2)

def grid_to_board(grid):
    board = {}
    for r in range_len(grid):
        for c in range_len(grid[0]):
            if grid[r][c] > 0:
                board[(r, c)] = {'rem': grid[r][c], 'bridges': {}}
    return changed_obj(board, fill_poss_cons)

def connections(board, node):
    cons = []
    for n in board[node]['poss']:
        if board[node]['poss'][n] < 2:
            cons += [n]
    return cons

def update_poss_count(board, n1, n2, new_count):
    board[n1]['poss'][n2] = new_count
    board[n2]['poss'][n1] = new_count

def rem_poss(board, node):
    total = 0
    for con in board[node]['poss']:
        total += board[node]['poss'][con]
    return total

def copy_board(board):
    copy = copy_2d_dict(board)
    for n in copy:
        copy[n]['poss'] = dict.copy(board[n]['poss'])
        copy[n]['bridges'] = dict.copy(board[n]['bridges'])
    return copy

def bridge_points(n1, n2):
    def dir(c): return 1 if n1[c] < n2[c] else (-1 if n1[c] > n2[c] else 0) # the parens are not neccessary
    x_dir = dir(0); y_dir = dir(1)
    points = [[]]
    def rec(n):
        new_n = (n[0] + x_dir, n[1] + y_dir)
        if not new_n == n2:
            points[0] += [new_n]
            rec(new_n)
    rec(n1)
    return points[0]

def board_to_grid(board):
    first = first_node(board)
    last = last_node(board)
    grid = []
    for x in range(first[0], last[0] + 1):
        row = []
        for y in range(first[1], last[1] + 1):
            n = 0 if not (x, y) in board else board[(x, y)]['rem']
            row += [n]
        grid += [row]
    return grid

def test_board_to_grid():
    """
    >>> board = grid_to_board(board_grid)
    >>> grid = board_to_grid(board)
    >>> grid == board_grid
    True
    """

def board_space_to_str(space):
    return ' ' if space == 0 else str(space)

def board_grid_to_str(bg):
    s = ''
    for row in bg:
        for space in row:
            s += board_space_to_str(space) + ' '
        s += '\n'
    return s

def board_to_str(board):
    return board_grid_to_str(board_to_grid(board))

def test_board_to_str():
    """
    >>> print(board_grid_to_str(board_grid))
    3   3   3   
      3   1     
    3         1 
      4     5   
    3         2 
          1     
    3       2   
      3   4   2 
    3   2   1   
    <BLANKLINE>
    """

testmod()
