# Class implementing Actor 
# based on a simple dictionary with some additional wrap around logic
#
#
# Policy .
import random 

class Actor:

    policy = {} #(t.state,action)
    eligibilities = {}  # (t.state,action), state as bitstring, action as (node_id, Direction)
    
    def __init__(self):
        self.eligibilities = {}

    
    def reset_eligibilities(self):
        self.eligibilities = {}
    
    def get_eligibilities(self,state_action_tup):
        if state_action_tup not in self.eligibilities.keys():
            self.eligibilities[state_action_tup] = random.random()*0.01
        return self.eligibilities[state_action_tup]
            
    def update_eligibilities(self,state_action_tup,gamma,delta):
        self.eligibilities[state_action_tup] = 1
        for key in self.eligibilities.keys():
            if key != state_action_tup:
                self.eligibilities[key] = self.eligibilities[key]*gamma*delta

    def get_policy(self,state_action_tup):
        if state_action_tup not in self.policy.keys():
            self.policy[state_action_tup] = 0
        return self.policy[state_action_tup]

    def set_policy(self,state_action_tup, value):
        if state_action_tup not in self.policy.keys():
            self.policy[state_action_tup] = 0
        self.policy[state_action_tup] = value

    def choose_action(self, state, actions, epsilon ):
        actions_values = {} # actions from a given state, on form {(state, dir), value }
        for action in actions:
            sap = (state, action)
            action_values[sap] = self.get_policy(sap)
        if len(actions_values) > 0 : #we must have some possible actions
            if random.random() < epsilon:
                return random.choice(list(action_values.keys()))[1]
            return max(actions_values.iterkeys(), key=(lambda x: actions_values[x]))



    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def get_epsilon(self):
        return epsilon


