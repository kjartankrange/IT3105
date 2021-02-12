from random import *
import math


def train(starting_state): #pseudocode page 9
    values = {starting_state: random.random()*0.1}
    
    policy = {} #mapping from state to action

    for episode in episodes: #iterate through all episodes
        actions = starting_state.get_available_moves() #get possible moves
        state = starting_state
        for action in actions: #iterate through moves
            policy[(state, action)] = 0
        action_s = [] 
        
        
        for t in episode:
            state.move(boltzmann_scaling_choice(state, policy)) #pick move from distribution
            boltzmann_scaling_choice(s)

        """
        eligibilities = 1
        if starting_state != previous_state:
            eligibilites = gamma delta eligibilites
        """
    
def boltzmann_scaling_choice(state, policy):
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


#def eligibiilteis