from sudoku_generator import *

def run():
    print('How difficult would you like your board to be: easy, medium, hard, or custom?')
    level = input()
    diff = None
    if   level == 'easy' or level == 'Easy':
        diff = (5, 0, 0)
    elif level == 'medium' or level == 'Medium':
        diff = (8, 2, 1)
    elif level == 'hard' or level == 'Hard':
        diff = (30, 4, 3)
    elif level == 'custom' or level == 'Custom':
        i_d = custom_inference_depth()
        m_o = custom_look_ahead_max_options()
        l_d = custom_look_ahead_depth()
        diff = (i_d, m_o, l_d)
    else:
        print('please enter one of the options given.')
        run()
    if diff is None: raise Exception('diff is None')
    # print(board_to_str(gen_board_level(diff)))
    print_board(diff, 5)

def print_board(diff, i):
    if not i == 0:
        board = gen_board_level(diff)
        count = 0
        for r in range(9):
            for c in range(9):
                if not board[r][c] == 0:
                    count += 1
        print('\n' + board_to_str(board))
        print('count: ' + str(count))
        print_board(diff, i - 1)

def custom_inference_depth():
    print('what do you want the maximum inference depth to be?')
    i_d = input()
    try: return int(i_d)
    except:
        print('please enter a number')
        custom_inference_depth()

def custom_look_ahead_max_options():
    print('what do you want the maximum number of options for looking ahead to be?')
    m_o = input()
    try: return int(m_o)
    except:
        print('please enter a number')
        custom_look_ahead_max_options()

def custom_look_ahead_depth():
    print('what do you want the maximum looking ahead depth to be?')
    l_d = input()
    try: return int(l_d)
    except:
        print('please enter a number')
        custom_look_ahead_depth()
    
run()