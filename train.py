from random import *
import math
from actor import Actor
from board import *
from actor import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from Visualisation import *
from time import sleep


random.seed(100)

class Player:

    def __init__(self, actor, board, critic_type):
        self.actor = actor
        self.board = board
        self.critic_type = critic_type
        
    
        if self.critic_type == 1: # use NNcritic
            from neural_net_critic import NeuralNetCritic
            state = board.state()
            input_layer_size = len(state)
            self.critic = NeuralNetCritic(alpha_c, lamda, gamma, dimNN, input_layer_size)
        else:
            from table_critic import Table_critic
            self.critic = Table_critic()

        
        #make visualisation later.

    def train(self, starting_state, gamma, alpha_a, alpha_c, l, epsilon, epsilon_deg,
              no_episodes):  # correct function name? should return the actors policies
        
        if critic_type==0:
            self.critic.create_value(starting_state.state())
        plot_data = []
        x_axis = []
        from tqdm import tqdm #progressbar
        for x in tqdm(range(no_episodes)):
            self.actor.reset_eligibilities()
            self.critic.reset_eligibilities()
            t = copy.deepcopy(starting_state)
            SAP = []
            s = t.state()
            while t.check_game_score() == 0:
                actions = t.get_available_moves()
                action = self.actor.choose_action(s, actions, epsilon)  # pick move from distribution
                SAP.append((s, action))
                t = t.move(action)
                s_prime = t.state() #s prime is (new) state, s is last state

                if self.critic_type==1: 
                    delta = float(self.critic.calc_td_error(t.check_game_score(), s_prime,s))
                    self.critic.fit(t.check_game_score(), s, s_prime, delta)
                else:
                    if not self.critic.get_value(s_prime):  # critic.get_values(s_prime)
                        self.critic.create_value(s_prime)
                    delta = t.check_game_score() + gamma * self.critic.get_value(s_prime) - self.critic.get_value(s)
                    if not self.critic.get_eligibilities(s): #s
                        self.critic.set_value(s,1)
                for tup in SAP:
                    if self.critic_type==0: 
                        value = self.critic.get_value(tup[0])+alpha_c*delta*self.critic.get_value(tup[0])
                        self.critic.set_value(tup[0], value)
                        eligibility = gamma*lamda*self.critic.get_eligibilities(tup[0])
                        self.critic.set_eligibility(tup[0],eligibility)
                    policy = actor.get_policy(tup) + alpha_a * delta * actor.get_eligibilities(tup)
                    if self.critic_type==1: 
                        actor.set_policy(tup, policy)
                        actor.update_eligibilities(tup, gamma, l)
                    else:
                        actor.set_policy(tup, policy)
                        actor.update_eligibilities(tup, gamma, l)
                
                s = s_prime
            epsilon *= epsilon_deg

            
            plot_data.append(len(t.find_alive_nodes()))
            x_axis.append(x)

          

        fig, ax = plt.subplots()
        ax.plot(x_axis, plot_data)
        #print(plot_data)

        if critic_type == 1: 
            crit_text = "Neural Net"
        else:
            crit_text = "Table-Critic"
        ax.set(xlabel='Episode', ylabel='Amount of pegs',
            title=crit_text)


        ax.grid()
        plt.show()
        if display:
            self.visualise(actor, starting_state, delay)  

    def visualise(self, actor_c, starting_state, delay):
            state = copy.deepcopy(starting_state)
            visualiser = Visualisation(state)
            vis = visualiser.visualise()
            plt.show()
            while state.check_game_score() == 0:
                visualiser.make_dead(state.get_board())
                vis = visualiser.visualise()
                if delay > 0:
                    plt.show(block = False)
                    plt.pause(delay)
                    plt.close()
                else: 
                    plt.show(block = True)

                action = actor_c.choose_action(state.state(), state.get_available_moves(), 0)
                state.move(action)
            visualiser.make_dead(state.get_board())
            vis = visualiser.visualise()
            plt.show()
        #visualiser = Visualisation(state)

#1) The type of Solitaire board: diamond or triangle.
type_of_board = "t" #"t" for triangle "d"for diamond
#2) The size of the board.
size_of_board = 5
#3) The open cell (or cells) in the puzzle’s start state.
#Center for t5: (2,1), (3,1), (3,2), for d4:(3,1), (3,2)
open_cells = [(2,1)] #just add more tuples for more holes. T5: (2,1), (3,2) D4: (3,1), (3,2)
#4) Number of episodes to run
episodes = 300 #no of episodes
#5) Whether the critic should use table lookup or a neural network.
critic_type = 1 # 0 is table critic, 1 is NN
#6) The dimensions of the critic’s neural network
dimNN = [5] #hidden layers in network
#7) The learning rates for the actor and critic
alpha_a = 0.7 #learning rate actor
alpha_c = 0.01 #learning rate critic
#8) The eligibility decay rate for the actor and critic
lamda = 0.85 # trace decay factor
#9) The discount factor for the actor and critic
gamma = 0.9 #discount factor
#10) The initial value of ε for the actor’s ε-greedy strategy and ε decay rate.
eps = 1 #epsilon
eps_deg = 0.9 #epsilon decay
#11) A display variable indicating when actual games will be visualized.
display = 1 #1 is visualize 0 is not
#12) The delay between frames of the game viewer.
delay = 0.3 #delay in seconds



actor = Actor()
starting_state = Board(type_of_board,size_of_board,open_cells) 
player = Player (actor , starting_state, critic_type)
player.train(starting_state,gamma,alpha_a,alpha_c,lamda , eps, eps_deg, episodes)



