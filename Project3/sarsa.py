from environment import Environment
from critic_net import Critic_net
import numpy as np
from tile_coder import get_flat_state 

from copy import deepcopy
import random
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from tqdm import tqdm #progressbar




class Player:

    def __init__(self, environment, critic):
        self.environment = environment
        self.critic = critic
        self.runs = {}
        self.wins = []
        
        #make visualisation later.

    def sarsa(self,  gamma, epsilon, epsilon_deg,
              no_episodes):  # correct function name? should return the actors policies
        
        plot_data = []
        x_axis = []
        count_wins = []
        count_loss = []
            
        for i in tqdm(range(no_episodes)):
            
            env = deepcopy(self.environment)
            self.runs[i] = []
            x = 0
            action_count=0
            action = 0
            losses = []
            while (not env.game_over()) and x<0.6:
                action_count+=1
                x = env.cart_x
                v = env.cart_velocity
                s = get_flat_state([x,v]) 
                self.last_state = s
                self.last_action = action 
                self.reward = env.reward()
                action = self.choose_action( [self.critic.forward(s,-1),self.critic.forward(s,0),self.critic.forward(s,1)] , epsilon)  # pick move from distribution
                
                env.update_velocity(action)
                
                x = env.cart_x
                
                v = env.cart_velocity
                
                s_prime = get_flat_state([x,v]) #s prime is (new) state, s is last state                
                
                action_prime = self.choose_action( [self.critic.forward(s_prime,-1),self.critic.forward(s_prime,0),self.critic.forward(s_prime,1)],epsilon )
                
                s_a_tup = (s,action)
                sp_ap_tup = (s_prime, action_prime)
                
                losses.append(self.critic.fit(s_a_tup, sp_ap_tup, env.reward(), gamma))

                s = s_prime
                
                if env.game_over == 1:
                    count_wins.append(1) 
                    if len(count_wins) > 10:
                        count_wins.pop(0)
                    print("W")
                    print( f"winrate: {sum(count_wins)/len(count_wins)}")
                
                if env.game_over() == -1:
                    count_wins.append(0)
                    if len(count_wins) > 10:
                        count_wins.pop(0)
                    print("L")
                    print( f"winrate: {sum(count_wins)/len(count_wins)}")
                self.runs[i].append(x)

            print(action_count," actions")
            epsilon *= epsilon_deg
            self.wins.append(action_count)
            #env.plot() 
            print("loss", sum(losses))
            plot_data.append(env.reward)
            x_axis.append(x)
            if True:
                with open("Data/datafil.txt","w") as f:
                    for x_value in self.runs[i]:
                        f.write(f"{x_value}\n")

        if plot:
            plt.scatter([z for z in range(no_episodes)], self.wins)
            plt.show()
        """
        #fig, ax = plt.subplots()
        #ax.plot(x_axis, plot_data)
        #print(plot_data)
   
        crit_text = "Neural Net"
       
        ax.set(xlabel='Episode', ylabel='Amount of pegs',
            title=crit_text)
        ax.grid()
        plt.show()
        if display:
            self.visualise(actor, starting_state, delay)  
        """
    def choose_action(self,QSas, epsilon):
        if random.random() < epsilon:
            return random.choice([-1,0,1])
        return np.argmax(QSas)-1
        """
        print(np.argmin(abs(QSas-(self.reward+self.critic.forward(self.last_state,self.last_action))))-1)
        for q in Qsas:    
            print(abs(q-(reward+self.critic.forward(self.last_state,self.last_action))))
        return np.argmin(abs(QSas-(self.reward+self.critic.forward(self.last_state,self.last_action))))-1
        """

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
    episodes = 100 #no of episodes

    #9) The discount factor for the actor and critic
    gamma = 0.9 #discount factor
    
    #10) The initial value of ε for the actor’s ε-greedy strategy and ε decay rate.
    eps = 1 #epsilon
    eps_deg = 0.95 #epsilon decay, 
    
    #11) A display variable indicating when actual games will be visualized.
    display = 1 #1 is visualize 0 is not

    #12) The delay between frames of the game viewer.
    delay = 0.3 #delay in seconds


    #6) The dimensions of the critic’s neural network
    dimNN = [] #hidden layers in network
    
    #7) The learning rates for the actor and critic
    learning_rate = 0.4 #learning rate critic

    activation_function = "r" 

    optimizer = "ad"   

    plot = True
    
    env = Environment()
    
    critic = Critic_net(learning_rate, 17 , dimNN, 1, activation_function, optimizer,"m","g","m")

    player = Player(env, critic)

    player.sarsa(gamma, eps, eps_deg, episodes)