class Node: 
    
    def __init__(self,alive,pos_x,pos_y): 
        self.alive = alive
        self.neighbours = []
        self.double_neighbours = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        
    def add_neighbour(self,lst):
        self.neighbour = lst
    
    def delete_neighbour(self,node):
        if(node in self.neigbours):
            self.neighbours = self.neighbours.remove(node)

    def kill(self):
        self.alive = 0
    
    def resurrect(self):
        self.alive = 1    
    
    