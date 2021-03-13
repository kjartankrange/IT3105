import random
class Table_critic():

    def __init__(self):
        self.eligibilities = {}
        self.values = {}
    
    def reset_eligibilities(self):
        self.eligibilities = {}
    
    def get_eligibilities(self,state):
        if state not in self.eligibilities.keys():
            return False
        return self.eligibilities[state]
    def set_eligibility(self, state, value):
        self.eligibilities[state] = value
            
    def decay_refresh_eligibilities(self,state,gamma,l):
        #self.eligibilities[state] = 1
        for key in self.eligibilities.keys():
            self.eligibilities[key] = self.eligibilities[key]*gamma*l

    def get_value(self,state):
        if state not in self.values.keys():
            return False
        return self.values[state]

    def set_value(self,state, value):
        self.values[state] = value
    
    def create_eligibilities(self, state):
        self.eligibilities[state] = 0

    def create_value(self, state):
        self.values[state] = random.random()

 