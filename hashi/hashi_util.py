from enum import Enum
from math import dist
from random import random, shuffle

# hashi specific util

class hard_enough(Enum):
    EASY = {'max_inference_depth': 1, 'max_sols_len': 1, 'max_look_ahead_depth': 0, 'max_look_ahead_sols': 0}
    HARD = {'max_inference_depth': 1, 'max_sols_len': 3, 'max_look_ahead_depth': 0, 'max_look_ahead_sols': 0}

class difficulty(Enum):
    EASY = {'max_inference_depth': 3, 'max_sols_len': 3, 
            'max_look_ahead_depth': 0, 'max_look_ahead_sols': 0, 'hard_enough_pars': hard_enough.EASY}
    HARD = {'max_inference_depth': 2, 'max_sols_len': 3, 
              'max_look_ahead_depth': 0, 'max_look_ahead_sols': 0, 'hard_enough_pars': hard_enough.HARD}

# temperary constants

dist_degrading_factor = 0.95
node_degrading_factor = 0.95

# general util

def changed_obj(o, f):
    f(o)
    return o

def pick_weighted(options):
    total_weight = 0
    for o in options: total_weight += o[1]
    choice = random()
    prev_weight = 0
    for o in options:
        if choice < (o[1] + prev_weight) / total_weight:
            return o[0]
        else: prev_weight += o[1]

def add_option_to_weighted_list(options, new_option, degrading_factor):
    for o in options:
        o[1] *= degrading_factor
    options += [[new_option, 1]]

def copy_2d_list(l):
        copy = []
        for i in l:
            copy += [list.copy(i)]
        return copy

def copy_2d_dict(d):
    copy = {}
    for k in d:
        copy[k] = dict.copy(d[k])
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

def str_equal_ignore_caps(s1, s2):
    return s1.upper() == s2.upper()