import numpy as np
import matplotlib.pyplot as plt



class Environment: 

    def __init__(self, cart_start_pos=(np.random.random()*0.2*-1 -0.4), cart_start_velocity=0): 
        self.cart_x = cart_start_pos
        self.cart_velocity = cart_start_velocity
        self.t = 0
        self.cart_positions = []
    
    def _update_location(self):
        self.cart_x += self.cart_velocity
        if self.cart_x >= 0.6:
            self.cart_x = 0.6

        elif self.cart_x <= -1.2:
            self.cart_x = -1.2
            self.cart_velocity = - self.cart_velocity  #3*(0.001*5 + -0.0025*np.cos(3*self.cart_x))

        
        self.save_values()
        
    def update_velocity(self, action):
        velocity = self.cart_velocity +0.001*action + -0.0025*np.cos(3*self.cart_x)
        self.cart_velocity = velocity if np.abs(velocity) < 0.07 else velocity/np.abs(velocity)*0.07
        self.t += 0.001
        self._update_location()   
    
    def reward(self):
        if self.cart_x >= .6:
            print("OOOOMGMGGGG we MADE IT!!!!!")
            return 0
        if self.t < 1:
            return -2*self.t -5/(0.01+1/2 * (1+self.cart_velocity)**2 + 10*(1+np.cos(3*(self.cart_x+np.pi/2))))-1
        print("Ouffff we lost")
        return -100
    def game_over(self):
        if self.t < 1:
            return 0
        if self.cart_x >= 0.6:
            return 1
        return -1

    def plot(self):
        all_x = np.arange(-1.2,0.6,0.001)
        all_y = np.cos(3*(all_x+np.pi/2))
        plt.plot( all_x, all_y )
        plt.plot( [self.cart_x], [np.cos(3*(self.cart_x+np.pi/2))],"ro") 
        plt.show(block=False)
    
    def save_values(self):
        self.cart_positions.append(self.cart_x)
    
    def plot_round(self):
        for i in range(len(self.cart_positions)):
            x_pos = self.cart_positions[i]
            plt.plot( [x_pos], [np.cos(3*(x_pos+np.pi/2))],"ro",color="red") 
        
        plt.plot( all_x, all_y )


