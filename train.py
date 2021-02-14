from random import *
import math
from board import *
from game import *

def train(starting_state, gamma, alpha_a, alpha_c, lamda): #pseudocode page 9
    values = {starting_state: random()*0.1}
    
    policy = {} #mapping from state to action
    
    for x in range(10): #iterate through all episodes
        eligibilities = {}
        eligibilities_critic = {}
        actions = starting_state.get_available_moves() #get possible moves
        t = starting_state
        for action in actions: #iterate through moves
            policy[(t.state(), action)] = 0
        action_s = [] 
        
        SAP = [()]
        
        while t.check_game_score() == 0:
            last_action = boltzmann_scaling_choice(t.state(), policy) #pick move from distribution
            last_state = t.state()
            SAP.append((last_state, last_action))
            t = t.move(action) 
            eligibilities[t.state(), action] = 1
            delta = t.check_game_score() + gamma*values[t.state()]-values[last_state]
            eligibilities_critic[last_state]=1
        
            for tup in SAP:
                values[tup[0]] += alpha_c*delta*eligibilities_critic[tup[0]]
                eligibilities_critic[tup[0]] = gamma*lamda*eligibilities_critic[tup[0]]
                policy[tup]=policy[tup] + alpha_a*delta*eligibilities[tup]
                eligibilities[tup] = gamma*lamda*eligibilities[tup]

            state = last_state
            action = last_action
            

def boltzmann_scaling_choice(state, policy): #Make a weighted choice on policy
    actions = state.get_available_moves()
    weights = []
    distribution = []
    sum1 = 0
    for action in actions:
        ai = math.e**(policy[(state, action)])
        weights.append(ai)
        distribution.append(ai)
        sum1 = ai
    for i in range(len(weights)):
        weights[i] = weights[i]/sum1
    draw = random.choices(actions, distribution, k=1)

    return draw



starting_state = Board("t",4,[(2,2)])
gamma = 0.9
alpha_a = 0.1
alpha_c = 0.1
lamda = 0.5 

train(starting_state,gamma,alpha_a,alpha_c,lamda)

