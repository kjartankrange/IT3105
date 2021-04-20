import numpy as np
import matplotlib.pyplot as plt

class Environment: 

    def __init__(self, time_step, cart_start_pos=(np.random.random()*0.2 - 0.4), cart_start_velocity=0): 
        self.cart_x = cart_start_pos
        self.cart_velocity = cart_start_velocity
        self.t = 0
        self.time_step = time_step
        self.cart_positions = []
    
    def update_location(self):
        self.cart_postions += self.cart_velocity
        self.save_values()
        
    def update_velocity(self, action):
        velocity = self.cart_velocity +0.001*action + -0.0025*np.cos(3*self.cart_postions)
        self.cart_velocity = velocity if np.abs(velocity) < 0.07 else velocity/np.abs(velocity)*0.07
    
    def reward(self):
        if self.cart_postions == .6:
            return 1
        if self.t/self.time_step < 1:
            return 0 
        else:
            return -1

    def plot(self):
        all_x = np.arange(-1.2,0.6,self.time_step)
        all_y = np.cos(3*(all_x+np.pi/2))
        plt.plot( all_x, all_y )
        plt.plot( [self.cart_x], [np.cos(3*(self.cart_x+np.pi/2))],"ro") 
        plt.show()
    
    def save_values(self):
        self.cart_positions(cart_velocity)

if __name__ == "__main__":
    env = Environment(0.01)
    env.plot()
    pass