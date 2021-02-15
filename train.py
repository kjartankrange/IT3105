from random import *
import math
from board import *
from game import *
from actor import *

class Player :

    def __init__(self, actor, critic, board, no_episodes):
        self.actor = actor,
        self.critic = critic,
        self.board = board
        self.no_episodes = no_episodes
        #make visualisation later.


    def train(self, starting_state, gamma, alpha_a, alpha_c, l): #correct function name? should return the actors policies

        values = {starting_state.state(): random.random() * 0.01} #remove later

        for x in range(self.no_episodes):
            actor.reset_eligibilities()
            t = starting_state
            eligibilities_critic = {} ## Reset eligibilities
            SAP = []
            s = t.state()
            count = 0
            while t.check_game_score() == 0:

                action = self.boltzmann_scaling_choice(t, actor)  # pick move from distribution
                SAP.append((s, action))
                t = t.move(action)
                s_prime = t.state()

                if s_prime not in values.keys(): # critic.get_values(s_prime)
                    values[s_prime] = random.random() * 0.01
                delta = t.check_game_score() + gamma * values[s_prime] - values[s]
                eligibilities_critic[(s, action)] = 1

                for tup in SAP:

                    values[tup[0]] += alpha_c * delta * actor.get_eligibilities(tup)

                    eligibilities_critic[tup] = gamma * l * eligibilities_critic[tup]
                    policy = actor.get_policy(tup) + alpha_a * delta * actor.get_eligibilities((s,action))
                    actor.set_policy((s,action), policy)
                    actor.update_eligibilities(tup, gamma, l)
                count += 1
                s = s_prime




    def boltzmann_scaling_choice(self, state, policy): #Make a weighted choice on policy
        actions = state.get_available_moves()
        weights = []
        distribution = []
        sum1 = 0
        for action in actions:
            ai = math.e**(actor.get_policy((state.state(),action)))
            weights.append(ai)
            distribution.append(ai)
            sum1 = ai
        for i in range(len(weights)):
            weights[i] = weights[i]/sum1
        draw = random.choices(actions, distribution, k=1)
        return draw[0]



starting_state = Board("t",4,[(2,2)])
gamma = 0.9
alpha_a = 0.1
alpha_c = 0.1
lamda = 0.5 

actor = Actor()
player = Player (actor, None, starting_state, 100)
player.train(starting_state,gamma,alpha_a,alpha_c,lamda)

