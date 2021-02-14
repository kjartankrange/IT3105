# Class implementing Actor 
# based on a simple dictionary with some additional wrap around logic
#
#
# Policy .
import random 

def class Actor():
    
    def __init__(self):
        self.eligibilities = {} , # (t.state,action)
        self.policy = {}, #(t.state,action)  
    
    def reset_eligibilities(self):
        eligibilities = {}
    
    def get_eligibilities(self,state_action_tup):
        if state_action_tup not in eligibilities.keys():
            eligibilities[tup] = random.random()*0.01 
        return eligibilities[tup]
            
    def update_eligibilities(self,state_action_tup,gamma,delta):
        eligibilities[state_action_tup] = 1 
        for key in eligibilities.keys():
            if key != state_action_tup:
                eligibilities[key] = eligibilities[key]*gamma*delta

    def get_policy(self,state_action_tup):
        if state_action_tup not in policy.keys():
            policy[tup] = random.random()*0.01 
        return policy[tup]
    

