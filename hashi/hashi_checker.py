from hashi_board import *
from hashi_util import *

def full(board):
    full = True
    for node in board:
        full &= board[node]['rem'] == 0
    return full

# connected:
#   visited = []
#   recursively traverse the graph (depth first) only visiting new nodes, and add each node visited
#   to visited. Stop when visited has every node, or the path has ended.

def connected(board):
    visited = [[]]
    def done(): return len(visited[0]) == len(board)
    def rec_search(node):
        if not done():
            visited[0] += [node]
            for n in connections(board, node):
                if not n in visited[0]:
                    rec_search(n)
    rec_search(list(board)[0])
    return done()


def solved(board):
    return full(board) and connected(board)