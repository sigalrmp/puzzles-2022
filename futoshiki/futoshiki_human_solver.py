from futoshiki_util import *
from futoshiki_checker import *

# NOTE: notes infrastructure

def relationships(board, r, c):
    l = board_len(board)
    rels = {'<': [], '>': []}
    def update_rels(rel, pos):
        if   rel == '<':
            rels['<'] += [pos]
        elif rel == '>':
            rels['>'] += [pos]
    if not r == 0:
        above_rel_raw = board[board_type.VER_INEQ][r - 1][c]
        above_rel = opp_ineq(above_rel_raw)
        update_rels(above_rel, (r - 1, c))
    if not r == l - 1:
         below_rel = board[board_type.VER_INEQ][r][c]
         update_rels(below_rel, (r + 1, c))
    if not c == 0:
        left_rel_raw = board[board_type.HOR_INEQ][r][c - 1] 
        left_rel = opp_ineq(left_rel_raw)
        update_rels(left_rel,  (r, c - 1))
    if not c == l - 1:
        right_rel = board[board_type.HOR_INEQ][r][c]
        update_rels(right_rel, (r, c + 1))
    for key in rels:
        rels[key] = tuple(rels[key])
    return rels

def board_to_notes(board):
    l = board_len(board)
    notes = {}
    for r in range(l):
        for c in range(l):
            rels = relationships(board, r, c)
            options = space_options(board, r, c)
            notes[(r, c)] = (options, rels)
    return notes

def notes_to_num_board(notes):
    l = notes_len(notes)
    num_board = empty_grid_list(l, l)
    for r in range(l):
        for c in range(l):
            space_opts = notes[(r, c)][0]
            if len(space_opts) == 1:
                num_board[r][c] = space_opts[0]
    return num_board

def notes_full(notes):
    full = True
    for i in notes:
        full = full and len(notes[i][0]) == 1
    return full

def notes_options(notes, space_pos):
    return notes[space_pos][0]

def notes_rels(notes, space_pos):
    return notes[space_pos][1]

def annotate(notes, space_pos, elim_opt):
    options = notes_options(notes, space_pos)
    if elim_opt in options:
        if len(options) == 1:
            crash_data = { 'bug': 'removing last option of space',
                           'space': space_pos,
                           'options before removal': options }
            raise Exception(dict_to_str(crash_data))
        options.remove(elim_opt)

def annotate_list(notes, space_pos, elim_opts):
    for n in elim_opts:
        annotate(notes, space_pos, n)

def notes_len(notes):
    return int(len(notes) ** 0.5)

def highest_option(notes, space_pos):
    opts = notes_options(notes, space_pos)
    return opts[len(opts) - 1]

def lowest_option(notes, space_pos):
    opts = notes_options(notes, space_pos)
    # if len(opts) == 0:
    #     print('wft. opts for pos is of length 0. pos: ' + str(space_pos))
    #     crash_info = { 'space_pos': space_pos }
    #     raise Exception(notes_to_str(notes))
    return opts[0]

def copy_rels(rels):
    copy = {}
    for ineq in rels:
        copy[ineq] = tuple(list.copy(list(rels[ineq])))
    return copy

def copy_notes(notes):
    copy = {}
    for s in notes:
        copy[s] = (list.copy(notes_options(notes, s)), 
                   copy_rels(notes_rels(notes, s)))
    return copy
            
def notes_to_str(notes):
    s = ''
    for space in notes:
        s += '  ' + str(space) + ': ' +  str(notes_options(notes, space)) + '\n'
        rels_s = dict_to_str(notes_rels(notes, space))
        s += rels_s
    return s

def notes_to_str_nums(notes):
    s = ''
    for space in notes:
        s += str(space) + ': ' + str(notes_options(notes, space)) + '\n'
    return s

# NOTE: inferences

# inferences:
#   1. For any spaces a and b such that a > b
#       - a cannot have any options that are lower than the lowest option for b
#   2. For any spaces a and b such that a < b
#       - a cannot have any options that are greater than the greatest option for b
#   3. if there are n places in a section that have the same n options AND NO OTHERS
#       - no other spaces in that section can have those options 
#   4. if there are n options in a section that ONLY appear in the same n spaces
#       - those spaces cannot have any other options

def first_and_second_inference(notes):
    l = notes_len(notes)
    for r in range(l):
        for c in range(l):
            pos = (r, c)
            rels = notes_rels(notes, (r, c))
            lowest = lowest_option(notes, pos)
            highest = highest_option(notes, pos)
            for lt_pos in rels['>']:
                # if len(notes_options(notes, lt_pos)) == 0:
                #     crash_infos = { 'bug': 'the lesser space has no options',
                #                        'called from': 'first_and_second_inference',
                #                        'pos': pos, 'lesser_pos': lt_pos,
                #                        'notes': '\n' + notes_to_str(notes) }
                #     raise Exception(dict_to_str(crash_infos))
                while lowest <= lowest_option(notes, lt_pos):
                    annotate(notes, pos, lowest)
                    # if len(notes_options(notes, pos)) == 0:
                    #     crash_info = { 'bug': 'removed all options by removing lowest',
                    #                    'called from': 'first_and_second_inference',
                    #                    'option removed': lowest,
                    #                    'condition of removal': str(lowest) + ' (lowest of pos) <= ' + 
                    #                                            str(lowest_option(notes, lt_pos)) + ' (lowest of lesser pos)',
                    #                    'pos': pos, 'lesser_pos': lt_pos }
                    #     raise Exception(dict_to_str(crash_info))
                    lowest = lowest_option(notes, pos)
            for gt_pos in rels['<']:
                while highest >= highest_option(notes, gt_pos):
                    annotate(notes, pos, highest)
                    highest = highest_option(notes, pos)

def third_inference_section(notes, section):
    l = notes_len(notes)
    section_list = section_to_list(section, l)
    for s in section_list:
        s_opts = notes_options(notes, s)
        tracker = [s] # list of spaces with the same options as s
        for s_ in section_list:
            if (not s_ == s) and notes_options(notes, s_) == s_opts:
                # tracker += [s_]
                tracker += [s_]
        if len(tracker) == len(s_opts):
            for s_ in section_list:
                if not s_ in tracker:
                    bug = True
                    for n in notes_options(notes, s_):
                        bug = bug and n in s_opts
                    if bug:
                        crash_data = { '\nbug': 'about to remove all opts from s_',
                                       'called from': 'third_inference_section',
                                       's_': s_,
                                       'what is being removed': s_opts,
                                       'tracker': tracker,
                                       'notes_options(notes, s_) == s_opts': notes_options(notes, s_) == s_opts,
                                       'notes': notes_to_str_nums(notes) }
                        raise Exception(dict_to_str(crash_data))
                    annotate_list(notes, s_, s_opts)

def third_inference(notes):
    for section in all_sections(notes_len(notes)):
        third_inference_section(notes, section)

def fourth_inference_section(notes, section):
    l = notes_len(notes)
    section_list = section_to_list(section, l)
    d = {}
    options = gen_options(l)
    for n in options:
        spaces = []
        d[n] = spaces
        for s in section_list:
            if n in notes_options(notes, s):
                spaces += [s]
    for n in options:
        tracker = [n] # list of options with the same spaces as n
        for n_ in range(n + 1, l + 1):
            if d[n_] == d[n]:
                tracker += [n_]
        if len(tracker) == len(d[n]):
            elim_opts = gen_options(l) # this needs to be separate from options
            for n_ in tracker:
                elim_opts.remove(n_)
            for s in d[n]:
                annotate_list(notes, s, elim_opts)

def fourth_inference(notes):
    for section in all_sections(notes_len(notes)):
        fourth_inference_section(notes, section)

inferences = (first_and_second_inference, third_inference, fourth_inference)

def infer(notes, depth):
    notes_copy = copy_notes(notes)
    if depth == 0:
        return depth
    for f in inferences:
        f(notes)
    if not (notes_full(notes) or notes_copy == notes):
        return infer(notes, depth - 1)
    else:
        return depth - 1

def look_ahead_h(notes, space, m):
    l = notes_len(notes)
    notes_copies = []
    space_opts = notes_options(notes, space)
    for i in range_len(space_opts):
        notes_copies += [copy_notes(notes)]
        elim_opts = list.copy(space_opts)
        elim_opts.remove(elim_opts[i])
        # debugging_info = {'called from': 'look_ahead_h','bug': 'all opts removed', 'space': space, 'space_opts': space_opts, 'elim_opts': elim_opts}
        annotate_list(notes_copies[i], space, elim_opts)
        # if len(notes_options(notes_copies[i], space)) == 0:
        #     raise Exception(dict_to_str(debugging_info))
        infer(notes_copies[i], m)
    for s in notes:
        for n in gen_options(l):
            remove = n in notes[s]
            for c in notes_copies:
                remove = remove and not n in c[s]
            if remove:
                annotate(notes, s, n)

def look_ahead(notes, n, m, start_index): # n is the max number of possibilities, m is the max depth for inferring
    l = notes_len(notes)
    space = None
    next_start_index = None
    for i in range(start_index, l ** 2):
        pos = num_board_index_to_pos(i, l)
        opt_count = len(notes_options(notes, pos))
        if 1 < opt_count <= n:
            space = pos
            if i < l ** 2 - 1:
                next_start_index = i + 1
            break
    if not space is None:
        look_ahead_h(notes, space, m)
        return next_start_index

def solve_like_human_h(notes, inference_depth, look_ahead_max_options, look_ahead_depth, look_ahead_start_index, recs):
    if inference_depth == 0:
        print('inferences ran out')
        return False
    remaining_inference_depth = infer(notes, inference_depth)
    if notes_full(notes):
        # print('board solved')
        return True
    else:
        if look_ahead_start_index is None:
            # print('ran out. times called: ' + str(recs))
            return False
        next_start_index = look_ahead(notes, look_ahead_max_options, look_ahead_depth, look_ahead_start_index)
        return solve_like_human_h(notes, remaining_inference_depth, look_ahead_max_options, look_ahead_depth, next_start_index, recs + 1)

def solve_like_human(notes_or_board, diff):
    (inference_depth, look_ahead_max_options, look_ahead_depth) = diff.value if type(diff) is difficulty else diff
    notes = notes_or_board if (0, 0) in notes_or_board else board_to_notes(notes_or_board)
    return solve_like_human_h(notes, inference_depth, look_ahead_max_options, look_ahead_depth, 0, 0)

# (r, c) -> i = l * r + c
# i -> (r, c) = 