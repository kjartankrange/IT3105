from board import *
from Visualisation import *
import random
from copy import deepcopy





def find_new_states(board, actions):
    states = {}
    for action in actions:
        new_state = result_function(board, action)
        states[action] = new_state
    print(states)
    return states


def result_function( board, action):
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


def main():

  shape,size,dead_pos = "t", 4, [(2,1),(2,2)]
  board = Board(shape,size,dead_pos)
<<<<<<< Updated upstream
  vis = Visualisation(board)
  while not check_game_score(board):
    moves = board.get_available_moves()
=======
  #vis = Visualisation(board)
  #show = vis.visualise()
  #plt.show()
  boards = []
  while not check_game_over(board):
      moves = board.get_available_moves()
      states = find_new_states(board, moves)
   # for board in states:
    #    for line in board.board:
     #       for node in line:
      #          print(node.alive, end="")
       #     print()
      m = random.choice((moves))
>>>>>>> Stashed changes


    #print(m)
      input("press enter for play: ")


      board = board.move(m)
      score = check_game_over(board)
      boards.append((states[m], score))
  for board in boards:
      print(board[0].state())
      print("score = " , board[1])
    #print(board.get_available_moves())

    #for line in board.board:
     #   for node in line:
      #      print(node.alive,end="")
       # print()

    #vis.make_dead(move)
    #show = vis.visualise()
    #plt.show()
main()


#shape,size,dead_pos = "t", 4, [(2,2)]
#board = Board(shape,size,dead_pos)
#actions = board.get_available_moves()
#new_states = find_new_states(board,actions)
#print(new_states)























#def run(shape,size,dead_pos_touples):
#  dead_pos_touples = [2,1]
 #   current_board = Board(shape,size,[(2,1)])
  #  vis = Visualisation(shape, size)

   # moves = [] #List with touple format: ([pos_x,pos_y],NE)
    #start_node = current_board.node_at(dead_pos)
    #start_node.double_neighbours.keys()

