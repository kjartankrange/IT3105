from board import *
from Visualisation import *
import random



def check_game_over(board): #returns if board is still playing, won, lost
    if len(board.get_available_moves())!=0:
        return 0 #game is not over
    elif board.node_count==1:
        return 1 #game is won
    else:
        return -1 #game is lost


def main():

  shape,size,dead_pos = "t", 4, [(1,0)]
  board = Board(shape,size,dead_pos)
  vis = Visualisation(board)
  while not check_game_over(board):
    moves = board.get_available_moves()

    m = random.choice((moves))

    #print(m)
    input("press enter for play: ")



    move = board.move(m)
    #print(board.get_available_moves())

    for line in board.board:
        for node in line:
            print(node.alive,end="")
        print()

    vis.make_dead(move)
    show = vis.visualise()
    plt.show()

main()























#def run(shape,size,dead_pos_touples):
#  dead_pos_touples = [2,1]
 #   current_board = Board(shape,size,[(2,1)])
  #  vis = Visualisation(shape, size)

   # moves = [] #List with touple format: ([pos_x,pos_y],NE)
    #start_node = current_board.node_at(dead_pos)
    #start_node.double_neighbours.keys()

