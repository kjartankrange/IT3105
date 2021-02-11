from node import * 
import copy
from node import *
from Visualisation import *

def make_triangle(size): #Helperfunction
    lst = []
    node_counter = 1
    for i in range(1,size+1):
        row = []
        for j in range(i):
            row.append(Node(1,node_counter))
            node_counter += 1
        lst.append(row)
    return lst



class  Board:
    opposite_directions = {"NE": "SW", "NW": "SE", "SW": "NE", "SE": "NW", "E": "W", "W": "E"}

        ## del opp i hjelpefunksjoner: make_board(), set_neighbours, set_doubleneighbours()
    def __init__(self,shape,size,dead_pos_touples):
        self.board = []
        self.node_count = 0
        self.size = size
        

        if shape == "t" and (size not in range(4,9)) or shape == "d" and (size not in range(3,7)):
            return "wrong initialization" 
        self.shape = shape
        
        if shape == "t":
            self.shape = shape
            self.board = make_triangle(size)

        elif shape == "d":
            lst = make_triangle(size)
            bottom_part = make_triangle(size)
            for  i in range(len(bottom_part)-2, -1, -1):
                lst.append(bottom_part[i])
            #lst.append(make_triangle(size)[:-1][::-1]) #trim of mid part and flip list on head
            self.board = lst
        #Øking: NW = [i-1,j-1] NE = [i-1,j] W = [i,j-1] E =[i,j+1] SW = [i+1,j] SE = [i+1,j+1]
        #Minking NW = [i-1,j] NE = [i-1,j+1] W = [i,j-1] E =[i,j+1] SW = [i+1,j-1] SE = [i+1,j] 
        for lst in self.board:
            for node in lst:
                self.node_count += 1
        #Add padding
        board_copy  = []
        for lst in self.board:
            row = []
            for node in lst:
                row.append(node)
            board_copy.append(row)
      
        for i in range(len(board_copy)):
            board_copy[i].append(None)
            board_copy[i].append(None)
            board_copy[i].insert(0,None)
            board_copy[i].insert(0,None)
        board_copy.append([None]*( len(self.board[-1]) + 4))
        board_copy.append([None]*( len(self.board[-1]) + 4))
        board_copy.insert(0,[None,None,None,None])
        board_copy.insert(0,[None,None,None,None])
     
        
        for i in range(len(self.board)):
            try: 
                increase = len(board[i+1]) -  len(board[i]) #finner halvdel av diamant
            except: 
                increase = 1 if shape == "t" else -1

            for j in range(len(self.board[i])):
                self.board[i][j].neighbours["W"] =  board_copy[i+2][j+2-1]
                self.board[i][j].neighbours["E"] =  board_copy[i+2][j+2+1]
                if increase == 1:

                    self.board[i][j].neighbours["NW"] =  board_copy[i+2-1][j+2-1]
                    self.board[i][j].neighbours["NE"] =  board_copy[i+2-1][j+2]
                    self.board[i][j].neighbours["SW"] =  board_copy[i+2+1][j+2]
                    self.board[i][j].neighbours["SE"] =  board_copy[i+2+1][j+2+1]
                else:

                    self.board[i][j].neighbours["NW"] =  board_copy[i+2-1][j+2]
                    self.board[i][j].neighbours["NE"] =  board_copy[i+2-1][j+2+1]
                    self.board[i][j].neighbours["SW"] =  board_copy[i+2+1][j+2-1]
                    self.board[i][j].neighbours["SE"] =  board_copy[i+2+1][j+2]
        #Set double neighbours
        """for i in range(len(self.board)):
            for j in range(len(self.board[i])): 
                node = self.board[i][j]
                for key in node.get_neighbours().keys():
                    if node.neighbours[key] != None:
                        node.get_double_neighbours()[key] = node.neighbours[key].neighbours[key]"""
        for lst in self.board:
            for node in lst:
                for key in node.neighbours.keys(): 
                    if isinstance(node.neighbours[key],Node): 
                        node.double_neighbours[key] = node.neighbours[key].neighbours[key]
        #set dead
        for touple in dead_pos_touples:
            x,y = touple
            self.board[touple[0]] [touple[1]] .kill()


    def get_nodes(self):  ## returns an array with the nodes in the board.
        nodes = []
        for row in self.board:
            for column in range(len(row)):
                nodes.append(row[column])
        return nodes

    def find_dead_nodes(self): #helper function for finding dead nodes. Returns the id of the nodes as a list
        nodes = self.get_nodes()
        dead_nodes = []
        for i in range(len(nodes)):
            if nodes[i].is_alive() == 0:
                dead_nodes.append(nodes[i])
        return dead_nodes

    def find_alive_nodes(self):
        dead_nodes = self.find_dead_nodes()
        alive_nodes = []
        nodes = self.get_nodes()
        for node in nodes:
            if node not in dead_nodes:  # should maybe be checked by id?
                alive_nodes.append(node)
        return alive_nodes

    def get_available_moves(self): #moves should be on form [Node, move_direction]
        ## We must concentrate on the dead nodes. Double neighbours can jump over neighbours,
        ## if the neighbour is alive.


        #find dead nodes, find their neighbours. if neighbours are alive and they have
        #double neighbours in same direction and double neighbour is alive, add to list
        moves = [] #moves on form {node_id : direction (from dead_node)}
        dead_nodes = self.find_dead_nodes()
        for node in dead_nodes:
            neighbours = node.get_neighbours()
            double_neighbours = node.get_double_neighbours()
            for neighbour in neighbours.items():
                if neighbour[1] is None:
                    continue
                if neighbour[0] in double_neighbours and neighbour[1].is_alive() and double_neighbours[neighbour[0]] is not None and double_neighbours[neighbour[0]].is_alive():


                    id = double_neighbours[neighbour[0]].get_id()##id
                    opposite_dir = neighbour[0]
                    direction = self.opposite_directions[opposite_dir]##direction
                    moves.append((id, direction))
        return moves

    def move(self, move):  # move on form (id, direction)
        nodes = self.get_nodes()
        id, dir = move
        node_to_move = nodes[id - 1]
        neighbours = node_to_move.get_neighbours()
        neighbour = neighbours[dir]
        double_neighbours = node_to_move.get_double_neighbours()
        double_neighbour = double_neighbours[dir]
        node_to_move.kill()
        neighbour.kill()
        double_neighbour.resurrect()
        self.node_count -= 1
        return self.get_board()

    def get_board(self):
        return self.board

    def get_shape(self):
        return self.shape

    def get_size(self):
        return self.size


         











    
"""

t4 = Board("t",4, [(1,0)] )
t4.find_alive_nodes()
vis = Visualisation(t4)
show = vis.visualise()
#print(t4.get_available_moves())
plt.show()



move = t4.move((9, "NW"))
vis.make_dead(move)
show = vis.visualise()
plt.show()



#print(t4.board[3][3].neighbours)
#print("\n")
#print(t4.board[0][0].double_neighbours)



#print(t4.board[6][0].neighbours)


#d5 = Board("d",5,[0,1])
#print(d5.board)
"""