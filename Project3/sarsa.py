from environment import Environment
from Project2 import action_net
import numpy as np


class Action_critic: 
    def __init__(self):
        state_pos_vel = {}
    
    def get_policy(position,velocity):
        if self.state_pos_vel.get((position,velocity)) == None: 
            self.state_pos_vel[(position,velocity)] = np.random.random()*0.01
        return self.state_pos_vel[(position,velocity)]

def sarsa(time_step, episodes, gamma):
    state_pos_vel = {}
    env = Environment(time_step)
    action(env.get_state())
    for episode in episodes:
        delta = env.reward() + gamma*net(env.state_action()) - net(env.last_state_action())



if __name__ == "__main__":
    time_step = 0.01


    sarsa()