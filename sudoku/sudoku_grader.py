from sudoku_util import *

options = gen_options()

def board_to_notes(board):
    notes = dict()
    for r in range(9):
        for c in range(9):
            options = space_options(board, r, c) if board[r][c] == 0 \
                      else [board[r][c]]
            notes.update({(r, c): options})
    return notes

def notes_to_board(notes):
    board = empty_board()
    for r in range(9):
        for c in range(9):
            space_opts = notes[(r, c)]
            if len(space_opts) == 1:
                board[r][c] = space_opts[0]
            else: board[r][c] = 0
    return board

def notes_full(notes):
    full = True
    for i in notes:
        full = full and len(notes[i]) == 1
    return full

# notes are initialized with every spot having every option unless it is an already given value

def annotate(space_pos, elim_opt, notes):
    # print('notes: ' + str(notes) + ', space_pos: ' + str(space_pos))
    if not type(notes) is dict:
        print('wtf. Notes (that is not a dict): ' + str(notes))
    options = notes[space_pos]
    if elim_opt in options:
        options.remove(elim_opt)

def annotate_list(space_pos, elim_opts, notes):
    for i in elim_opts:
        annotate(space_pos, i, notes)

# so how do I systematically do this?
# here are the first two things that I want to make it infer:
#   1. if there are n places in a section that have the same n options AND NO OTHERS then
#       - no other spaces in that section can have those options
#   2. if there are n options in a section that ONLY appear in the same n spaces then
#       - those spaces cannot have any other options
# strategies:
#   1. for each space in each section, count (starting at one so that the space is counted) how
#      many spaces in their section (that have not already been checked) have the same list 
#      of options as them (using ==), and if that count is equal to the length of the list,
#      remove all options in that list from all other spaces in that section
#   2. for each possible option i in each section, make a list of the spaces that they are an
#      option for. Then, for each i, count (starting at one so that the option is
#      counted) how many other options (that haven't been checked yet) have the same list of
#      spaces. If that count is equal to the length of the list, the spaces in that list cannot
#      have any options aside from those possible options

# inference functions

def first_inference_section(notes, section_spaces): # section_spaces is a list of all spaces in one section
    for si in range(9):
        s = section_spaces[si]
        # print('s: ' + str(s))
        tracker = [s] # list of spaces that have the same options as s
        for s_i in range(si + 1, 9):
            s_ = section_spaces[s_i]
            if notes[s_] == notes[s]:
                tracker += [s_]
        if len(tracker) == len(notes[s]):
            # print('replacing shit. s: ' + str(s))
            for s_ in section_spaces:
                if not s_ in tracker:
                    annotate_list(s_, notes[s], notes)
        # else: print('not replacing shit. s: ' + str(s) + ', tracker: ' + str(tracker) + ', options for s: ' + str(notes[s]))

def first_inference(notes): # untested!!
    for section in all_sections():
        section_spaces = section_to_list(section[0], section[1])
        first_inference_section(notes, section_spaces)

def second_inference_section(notes, section_spaces):
    d = {}
    for i in options:
        spaces = []
        d.update({i: spaces})
        for s in section_spaces:
            if i in notes[s]:
                spaces += [s]
    for i in options:
        tracker = [i] # list of options with the same spaces as i
        for i_ in range(i + 1, 10):
            if d[i] == d[i_]:
                tracker += [i_]
        if len(tracker) == len(d[i]):
            elim_opts = list(range(10))
            for i_ in tracker:
                elim_opts.remove(i_)
            for s in d[i]:
                annotate_list(s, elim_opts, notes)

def second_inference(notes):
    for section in all_sections():
        section_spaces = section_to_list(section[0], section[1])
        second_inference_section(notes, section_spaces)            

inferences = (first_inference, second_inference) # tuple of inference functions

def infer(notes, depth):
    notes_copy = copy_notes(notes)
    if (depth == 0):
        # print('cannot solve with only allotted inferences. returning depth: ' + str(depth))
        return depth
    for f in inferences: # I could replace this with: first_inference(notes) \ second_inference(notes)
        f(notes)
    if not (notes_full(notes) or notes_copy == notes):
        return infer(notes, depth - 1)
    else:
        return depth

def look_ahead_h(notes, space, m):
    notes_copies = []
    for i in range(len(notes[space])):
        notes_copies += [copy_notes(notes)]
        elim_opts = list.copy(notes[space])
        elim_opts.remove(elim_opts[i])
        # print('elim opts: ' + str(elim_opts))
        annotate_list(space, elim_opts, notes_copies[i])
        infer(notes_copies[i], m)
    for s in notes:
        for i in options:
            remove = i in notes[s]
            for c in notes_copies:
                remove = remove and not i in c[s]
            if remove:
                annotate(s, i, notes)


def look_ahead(notes, n, m, start_space): # n is the max number of possibilities, m is the max depth, first_pos is the first place you will use
    space = None
    next_start_space = None
    if not type(start_space) is tuple:
        print('wtf. start_space: ' + str(start_space))
    for r in range(start_space[0], 9):
        for c in range(9):
            if not (r == start_space[0] and c <= start_space[1]):
                if not space is None:
                    # print('changing next_space. space: ' + str(space) + '. next_space: ' + str((r, c)))
                    next_start_space = (r, c)
                    break
                opt_count = len(notes[(r, c)])
                if 1 < opt_count <= n:
                    # print('assigning space: ' + str((r, c)))
                    space = (r, c)
        if not next_start_space is None:
            break
    if not space is None:
        look_ahead_h(notes, space, m)
        return next_start_space

def solve_like_human_h(notes, inference_depth, look_ahead_max_options, look_ahead_depth, look_ahead_start_space):
    if inference_depth == 0:
        print('inferences ran out')
        return False
    # else: print('inference_depth: ' + str(inference_depth))
    # print('before anything:\n' + board_to_str(notes_to_board(notes)))
    remaining_inference_depth = infer(notes, inference_depth)
    # if not type(remaining_inference_depth) is int:
    #     print('what the actual fuck. the next inference depth is not an integer.')
    # print('last inference depth: ' + str(inference_depth))
    # print('next inference depth: ' + str(remaining_inference_depth))
    if remaining_inference_depth is None:
        print('fuck my life')
    # print('after infer:\n' + board_to_str(notes_to_board(notes)) + '\n')
    if notes_full(notes):
        print('board solved')
        return True
    else:
        if look_ahead_start_space is None: 
            # print('not starting anywhere')
            return False
        next_start_space = look_ahead(notes, look_ahead_max_options, look_ahead_depth, look_ahead_start_space)
        # print('after looking ahead:\n' + board_to_str(notes_to_board(notes)))
        return solve_like_human_h(notes, remaining_inference_depth, look_ahead_max_options, look_ahead_depth, next_start_space)

def solve_like_human(notes, inference_depth, look_ahead_max_options, look_ahead_depth):
    return solve_like_human_h(notes, inference_depth, look_ahead_max_options, look_ahead_depth, (0, 0))


#  finished:
#   - can do the two basic inferences
# to do:
#   - make it so once it's gotten as far as it can get like that, it goes through
#     all the situations where there are only n options (where n is different depending on the
#     difficulty) and in each of those situations, infers things up to m times (so not that deep)
#     compare the boards and if there is anything that all of the possible boards agree on, add
#     to the notes. Then start making inferences again. Continue doing this, and if it never works
#     the puzzle is too hard.