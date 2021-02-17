import random
class Table_critic():

    def __init__(self):
        self.eligibilities = {}
        self.values = {}
    
    def reset_eligibilities(self):
        self.eligibilities = {}
    
    def get_eligibilities(self,state):
        if state not in self.eligibilities.keys():
            self.eligibilities[state] = random.random()*0.001
        return self.eligibilities[state]
            
    def decay_refresh_eligibilities(self,state,gamma,l):
        self.eligibilities[state] = 1
        for key in self.eligibilities.keys():
            if key != state:
                self.eligibilities[key] = self.eligibilities[key]*gamma*l

    def get_values(self,state):
        if state not in self.values.keys():
            self.values[state] = 0
        return self.values[state]

    def set_values(self,state, value):
        if state not in self.values.keys():
            self.values[state] = 0
        self.values[state] = value

 