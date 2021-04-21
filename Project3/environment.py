import numpy as np
import matplotlib.pyplot as plt



class Environment: 

    def __init__(self, cart_start_pos=(np.random.random()*0.2*- -0.4), cart_start_velocity=0): 
        self.cart_x = cart_start_pos
        self.cart_velocity = cart_start_velocity
        self.t = 0
        self.cart_positions = []
    
    def _update_location(self):
        self.cart_x += self.cart_velocity
        self.cart_x = 0.6 if self.cart_x >= 0.6 else self.cart_x 
        self.save_values()
        
    def update_velocity(self, action):
        velocity = self.cart_velocity +0.001*action + -0.0025*np.cos(3*self.cart_postions)
        self.cart_velocity = velocity if np.abs(velocity) < 0.07 else velocity/np.abs(velocity)*0.07
        self.t += 0.001
        update_location()   
    
    def reward(self):
        if self.cart_postions == .6:
            print("OOOOMGMGGGG we MADE IT!!!!!")
            return 1
        if self.t < 1:
            return 0 
        else:
            return -1

    def plot(self):
        all_x = np.arange(-1.2,0.6,0.001)
        all_y = np.cos(3*(all_x+np.pi/2))
        plt.plot( all_x, all_y )
        plt.plot( [self.cart_x], [np.cos(3*(self.cart_x+np.pi/2))],"ro") 
        plt.show()
    
    def save_values(self):
        self.cart_positions.append(self.cart_x)

if __name__ == "__main__":
    env = Environment(0.01)
    env.plot()
    pass