class Node: 
    
    def __init__(self,alive, id):
        self.id = id
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
   
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = 0
    
    def resurrect(self):
        self.alive = 1  

    def get_neighbours(self):
        return self.neighbours

    def get_double_neighbours(self):    
        return self.double_neighbours


    
    