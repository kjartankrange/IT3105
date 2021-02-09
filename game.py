from board import *
def run(shape,size,dead_pos_touples):
    dead_pos_touples = [2,1]
    current_board = Board(shape,size,[(2,1)])
    moves = [] #List with touple format: ([pos_x,pos_y],NE)
    start_node = current_board.node_at(dead_pos)
    start_node.double_neighbours.keys()