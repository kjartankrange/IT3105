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

    def __init__(self, actor, critic, board, no_episodes):
        self.actor = actor
        self.critic = critic
        self.board = board
        self.no_episodes = no_episodes
        
    """
        if self.critic == 0: # use TableCritic
            from table_critic import TableCritic
            self.critic = TableCritic(alpha_c, lamda, gamma) #
        else: # use criticNN
            from neural_net import NeuralNetCritic
            state = board.state()
            inputLayerSize = len(state)
            self.critic = NeuralNetCritic(alpha_c, lamda, gamma, dimNN, inputLayerSize)
        """
        #make visualisation later.

    def train(self, starting_state, gamma, alpha_a, alpha_c, l, epsilon, epsilon_deg,
              no_episodes):  # correct function name? should return the actors policies
        
        values = {starting_state.state(): random.random()}  # remove later
        plot_data = []
        x_axis = []
        for x in range(no_episodes):
            actor.reset_eligibilities()
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

                if s_prime not in values.keys():  # critic.get_values(s_prime)
                    values[s_prime] = random.random()

                delta = t.check_game_score() + gamma * values[s_prime] - values[s]
                eligibilities_critic[s] = 1

                for tup in SAP:
                    values[tup[0]] += alpha_c * delta * eligibilities_critic[tup[0]]
                    eligibilities_critic[tup[0]] = gamma * l * eligibilities_critic[tup[0]]
                    policy = actor.get_policy(tup) + alpha_a * delta * actor.get_eligibilities(tup)
                    actor.set_policy((s, action), policy)
                    actor.update_eligibilities(tup, gamma, delta)
                s = s_prime
                epsilon *= epsilon_deg
            plot_data.append(len(t.find_alive_nodes()))
            x_axis.append(x)

        #vis = Visualisation(t)
        #show = vis.visualise()
        #plt.show()
            
        fig, ax = plt.subplots()
        ax.plot(x_axis, plot_data)
        
        ax.set(xlabel='Episode', ylabel='Amount of pegs',
        title='Test')

        ax.grid()
        plt.show()




starting_state = Board("t",4,[(2,2)])
gamma = 0.9
alpha_a = 0.1
alpha_c = 0.1
lamda = 0.5 
critic = 0 # 0 is table critic, 1 is NN

actor = Actor()
player = Player (actor, None , starting_state, 1000)
player.train(starting_state,gamma,alpha_a,alpha_c,lamda , 1.0, 0.9, 1000)

