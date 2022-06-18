from hashi_imports import *

def run():
    diff = custom_difficulty()
    print('the creation of the board may take a while')
    board = gen_board(diff=diff)
    print('\n' + board_to_str(board) + '\n')

def custom_difficulty():
    print('How difficult would you like your board to be: easy or hard (both will take a long time, but hard will be longer)?')
    level = input()
    if str_equal_ignore_caps(level, 'easy'):
        return difficulty.EASY
    elif str_equal_ignore_caps(level, 'hard'):
        return difficulty.HARD
    else:
        print('please enter one of the options given')
        custom_difficulty()
run()