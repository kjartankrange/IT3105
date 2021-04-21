from environment import Environment
from critic_net import Critic_net
import numpy as np


from random import *
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from tqdm import tqdm #progressbar



random.seed(100)

class Player:

    def __init__(self, environment, critic):
        self.environment = environment
        self.critic = critic
        
        
        #make visualisation later.

    def sarsa(self,  gamma, epsilon, epsilon_deg,
              no_episodes):  # correct function name? should return the actors policies
        
        self.critic.create_value(starting_state.state())
        plot_data = []
        x_axis = []
        for x in tqdm(range(no_episodes)):
            
            self.critic.reset_eligibilities() #gives backup to states, how often used, states
            env = copy.deepcopy(self.environment)
            s = env.state()
            action_count = 0
            
            while not env.reward():
                
                
                action = choose_action( [self.critic.forward(s,-1),self.critic.forward(s,0),self.critic.forward(s,1)] )  # pick move from distribution
                
                env = env.update_velocity(action)
                
                

                
                s_prime = env.state() #s prime is (new) state, s is last state                
                
                self.critic.fit(t.check_game_score(), s, s_prime, delta)
            
                s = s_prime
            epsilon *= epsilon_deg

            
            plot_data.append(len(t.find_alive_nodes()))
            x_axis.append(x)

          

        fig, ax = plt.subplots()
        ax.plot(x_axis, plot_data)
        #print(plot_data)

   
        crit_text = "Neural Net"
       
        ax.set(xlabel='Episode', ylabel='Amount of pegs',
            title=crit_text)


        ax.grid()
        plt.show()
        if display:
            self.visualise(actor, starting_state, delay)  
    
    def make_choice(QSas, epsilon):
        if random.random() < epsilon:
            return np.argmax(QSas)-1
        return random.choice([-1,0,1])
    

    def visualise(self, actor_c, starting_state, delay):
            state = copy.deepcopy(starting_state)
            visualiser = Visualisation(state)
            vis = visualiser.visualise()
            plt.show()
            while state.check_game_score() == 0:
                visualiser.make_dead(state.get_environment())
                vis = visualiser.visualise()
                if delay > 0:
                    plt.show(block = False)
                    plt.pause(delay)
                    plt.close()
                else: 
                    plt.show(block = True)

                action = actor_c.choose_action(state.state(), state.get_available_moves(), 0)
                state.move(action)
            visualiser.make_dead(state.get_environment())
            vis = visualiser.visualise()
            plt.show()
        #visualiser = Visualisation(state)





if __name__ == "__main__":
    



    #4) Number of episodes to run
    episodes = 20 #no of episodes

    #9) The discount factor for the actor and critic
    gamma = 0.9 #discount factor
    
    #10) The initial value of ε for the actor’s ε-greedy strategy and ε decay rate.
    eps = 1 #epsilon
    eps_deg = 0.9 #epsilon decay, 
    
    #11) A display variable indicating when actual games will be visualized.
    display = 1 #1 is visualize 0 is not

    #12) The delay between frames of the game viewer.
    delay = 0.3 #delay in seconds


    #6) The dimensions of the critic’s neural network
    dimNN = [] #hidden layers in network
    
    #7) The learning rates for the actor and critic
    alpha_c = 0.01 #learning rate critic

    activation_function = "r" 

    optimizer = "a"   
    
    
    env = Environment()
    
    net = Critic_net(learning_rate, 9 , dimNN, 1, activation_function, optimizer,"m","g","m")

    player = Player(env, critic_type)

    player.sarsa(gamma, eps, eps_deg, episodes)

