from board import *
from Visualisation import *
import random
import copy
from matplotlib import pyplot as plt





def find_new_states(board, actions): # returns a dictionary with states after (different) actions are applied
    states = {}
    for action in actions:
        new_state = result_function(board, action)
        states[action] = new_state
    return states


def result_function( board, action): #returns a new board after a specific action is applied
    cop = copy.deepcopy(board)
    new_state = cop.move(action)

    return new_state



def check_game_score(board): #returns if board is still playing, won, lost
    if len(board.get_available_moves())!=0:
        return 0 #game is not over
    elif board.node_count==1:
        return 1 #game is won
    else:
        return -1 #game is lost


def main(): # running the game with random moves.

    shape,size,dead_pos = "d", 4, [(2,2)]
    board = Board(shape,size,dead_pos)
    vis = Visualisation(board)
    show = vis.visualise()
    plt.show()
    boards = []
    while not check_game_score(board):
        moves = board.get_available_moves()
        states = find_new_states(board, moves)
        m = random.choice((moves))
        print(m)
        input("press enter for play: ")
        board = board.move(m)

        score = check_game_score(board)
        boards.append((states[m], score))
        vis.make_dead(board.get_board())
        show = vis.visualise()
        plt.show()

#main()