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
    def __init__(self,shape,size,dead_pos_touple): 

        if shape == "t" and (size not in [4,5,6,7,8]) or shape == "d" and (size not in [3,4,5,6]):
            return "wrong initialization" 
        self.shape = shape
        
        if shape == "t":
            self.shape = shape
            self.board = make_triangle(size)

        elif shape == "d":
            lst = make_triangle(size)
            lst.append(make_triangle(size)[:-1][::-1]) #trim of mid part and flip list on head
            self.board = lst
        #Øking: NW = [i-1,j-1] NE = [i-1,j] W = [i,j-1] E =[i,j+1] SW = [i+1,j] SE = [i+1,j+1]
        #Minking NW = [i-1,j] NE = [i-1,j+1] W = [i,j-1] E =[i,j+1] SW = [i+1,j-1] SE = [i+1,j] 
        
        #Add padding
        board_copy = copy.deepcopy(self.board)
        for i in range(len(board_copy)):
            board_copy[i].append(None)
            board_copy[i].append(None)
            board_copy[i].insert(0,None)
            board_copy[i].insert(0,None)
        board_copy.append([None]*( len(self.board[-1]) + 4))
        board_copy.append([None]*( len(self.board[-1]) + 4))
        board_copy.insert(0,[None,None,None,None])
        board_copy.insert(0,[None,None,None,None])
        """print("\n")
        for el in board_copy:
            print(el)
        """
        
        for i in range(len(self.board)):
            try: 
                increase = board[i+1] -  board[i]
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
        #Doubke neighbours
                
    
   
        
    
    


t4 = Board("t",4,[0,1])
print(t4.board[0][0].neighbours)
"print(t4.board)"
#d5 = Board("d",5,[0,1])
#print(d5.board)