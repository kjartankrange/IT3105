from random import *
import math
from actor import Actor
from board import *
from game import *
from actor import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Player:

    def __init__(self, actor, critic, board, criticType):
        self.actor = actor
        self.critic = critic
        self.board = board
        self.criticType = criticType
        
    
        if self.criticType == 1: # use NNcritic
            from neural_net import NeuralNetCritic
            state = board.state()
            inputLayerSize = len(state)
            self.critic = NeuralNetCritic(alpha_c, lamda, gamma, dimNN, inputLayerSize)

        """
        else: # use table critic
            from table_critic import TableCritic
            self.critic = TableCritic(alpha_c, lamda, gamma) 
        """
        
        #make visualisation later.

    def train(self, starting_state, gamma, alpha_a, alpha_c, l, epsilon, epsilon_deg,
              no_episodes):  # correct function name? should return the actors policies
        
        values = {starting_state.state(): random.random()}  # remove later
        plot_data = []
        x_axis = []
        from tqdm import tqdm
        for x in tqdm(range(no_episodes)):
            actor.reset_eligibilities()
            if self.criticType==1: 
                self.critic.resetEligibilities()
            t = copy.deepcopy(starting_state)
            eligibilities_critic = {}  ## Reset eligibilities
            SAP = []
            s = t.state()
            while t.check_game_score() == 0:
                actions = t.get_available_moves()
                action = actor.choose_action(s, actions, epsilon)  # pick move from distribution
                SAP.append((s, action))
                t = t.move(action)
                s_prime = t.state()

                if self.criticType==1: 
                    td_error = self.critic.findTDError(t.check_game_score(), s, s_prime)
                    self.critic.fit(t.check_game_score(), s, s_prime, td_error)
                else:

                    if s_prime not in values.keys():  # critic.get_values(s_prime)
                        values[s_prime] = random.random()

                    delta = t.check_game_score() + gamma * values[s_prime] - values[s]
                if s not in eligibilities_critic.keys():
                    eligibilities_critic[s] = 1

                for tup in SAP:
                    if self.criticType==0: 
                        values[tup[0]] += alpha_c * delta * eligibilities_critic[tup[0]]
                    eligibilities_critic[tup[0]] = gamma * l * eligibilities_critic[tup[0]]
                    if self.criticType==1: 
                        NNpolicy = actor.get_policy(tup) + alpha_a * td_error * actor.get_eligibilities(tup)
                        #self.critic.updateEligibilities()
                        actor.set_policy((s, action), NNpolicy)
                        actor.update_eligibilities(tup, gamma, l)
                    else:
                        policy = actor.get_policy(tup) + alpha_a * delta * actor.get_eligibilities(tup)
                        actor.set_policy((s, action), policy)
                        actor.update_eligibilities(tup, gamma, l)
                
                s = s_prime
            epsilon *= epsilon_deg

            plot_data.append(len(t.find_alive_nodes()))
            x_axis.append(x)
        vis = Visualisation(t)
        show = vis.visualise()
        plt.show()
            
        fig, ax = plt.subplots()
<<<<<<< HEAD
        ax.plot(x_axis, plot_data, 'ro')
        #print(plot_data)
=======
        ax.plot(x_axis, plot_data)
>>>>>>> facd8f34de071c454b758a807da823eb7ba096e3
        
        ax.set(xlabel='Episode', ylabel='Amount of pegs',
        title='Test')

        ax.grid()
        plt.show()




<<<<<<< HEAD
starting_state = Board("t",4,[(2,2)]) 
=======
starting_state = Board("t",4,[(3,1),(3,3)])
>>>>>>> facd8f34de071c454b758a807da823eb7ba096e3
gamma = 0.9
alpha_a = 0.7
alpha_c = 0.1
lamda = 0.8
critic = 1 # 0 is table critic, 1 is NN
eps = 1
<<<<<<< HEAD
eps_deg = 0.995
rounds = 700
dimNN = [5]
=======
eps_deg = 0.99
rounds = 4000
>>>>>>> facd8f34de071c454b758a807da823eb7ba096e3

actor = Actor()


player = Player (actor, None , starting_state, critic)
player.train(starting_state,gamma,alpha_a,alpha_c,lamda , eps, eps_deg, rounds)