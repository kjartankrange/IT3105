class Node: 
    
    def __init__(self,alive): 
        self.alive = alive
        self.neighbours = dict.fromkeys(["NE","NW","SE","SW","E","W"])
        self.double_neighbours = dict.fromkeys(["NE","NW","SE","SW","E","W"])

        
    def add_neighbour(self,node,pos):
        if node in self.neighbours.keys():
            raise Exception("Node is already a neighbour")
        self.neighbours[pos] = node  
   
    def add_double_neighbour(self,node,pos):
        if node in self.neighbours.values() or node in self.double_neighbours.values():
            raise Exception("Node is already a double_neighbour")
        self.double_neighbours[pos] = node
   
    def kill(self):
        self.alive = 0
    
    def resurrect(self):
        self.alive = 1  

    def get_neighbours(self):
        return self.neighbours

    def get_double_neighbours(self):    
        return self.double_neighbours
#  def delete_neighbour(self,node):
    #   if(node in self.neigbours):
    #        self.neighbours = self.neighbours.remove(node)

    
    