from node import * 
import copy

def make_triangle(size): #Helperfunction
    lst = []
    for i in range(1,size+1):
        row = []
        for j in range(i):
            row.append(Node(1))
        lst.append(row)
    return lst

class  Board:


    def __init__(self,shape,size,dead_pos_touples, isUpdate = False, move = None):
        self.board = []
        self.node_count = 0
        

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
                print(self.board[i][j])
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

<<<<<<< Updated upstream
         
    """
=======
        if(isUpdate and move is not None):

            self.node_count -= 1
            original_x, original_y = move[0]  ##list with x_position and y_position
            original_node = self.board[original_x][original_y]
            double_neighbours_original = original_node.get_double_neighbours()
            new_node = double_neighbours_original[move[1]]  # find the correct double neighbour using sky direction
            original_node.kill()
            new_node.resurrect()
            original_node.get_neighbours()[move[1]].kill()






    def is_legal_move(self,move): #move on format ([x_pos,y_pos], "Sky direction")
        if len(move) != 2:
            return False
        pos = move[0]
        if len(pos) != 2:
            return False
        x_pos, y_pos = pos
        sky_dir = move[1]
        if self.board[x_pos][y_pos].alive != 1:
            return False
        print(self.board[x_pos][y_pos])
        new_node = self.board[x_pos][y_pos].get_double_neighbours()[sky_dir]
        if new_node.alive != 0:
            return False
        jump_node = self.board[x_pos][y_pos].get_neighbours()[sky_dir]
        if jump_node != 1:
            return False
        return True


        

>>>>>>> Stashed changes
    def node_at(touple):
        return self.board[touple[0]][touple[1]]   
    """
   
    """
    def moves_board_score():
        pass
    """
    """def legal_moves():
        for lst in self.board:
            pass
        pass"""

    """def score():
        return (not self.legal_moves()) or (self.node_count == 1
        return (not self.legal_moves())*( (self.node_count ==1) - 1)"""

    
   
        
    
    


t4 = Board("d",4, [(1,0)])


#print(t4.board[3][3].neighbours)
#print("\n")
#print(t4.board[0][0].double_neighbours)


count = 0
for row in t4.board:
    print()
    for node in row:
        print(node.alive, end = "")
print(t4.board[6][0].neighbours)


#d5 = Board("d",5,[0,1])
#print(d5.board)