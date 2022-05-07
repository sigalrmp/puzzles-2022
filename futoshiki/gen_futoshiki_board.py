from ast import excepthandler
from futoshiki_imports import *

def run():
    l = custom_length()
    diff = custom_difficulty()
    board = gen_board_graded(l=l, diff=diff)
    print('\n' + board_to_str(board) + '\n')


def custom_length():
    print('What would you like the sidelength of your board to be?')
    l = input()
    try: return int(l)
    except:
        print('please enter a number')
        custom_length()

def custom_difficulty():
    print('How difficult would you like your board to be: easy, medium, hard, wicked, or custom?')
    level = input()
    if str_equal_ignore_caps(level, 'easy'):
        return difficulty.EASY
    elif str_equal_ignore_caps(level, 'medium'):
        return difficulty.MEDIUM
    elif str_equal_ignore_caps(level, 'hard'):
        return difficulty.HARD
    elif str_equal_ignore_caps(level, 'wicked'):
        return difficulty.WICKED
    elif str_equal_ignore_caps(level, 'custom'):
        i_d = custom_inference_depth()
        m_o = custom_look_ahead_max_options()
        l_d = custom_look_ahead_depth()
        return (i_d, m_o, l_d)
    else:
        print('please enter one of the options given')
        custom_difficulty()

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