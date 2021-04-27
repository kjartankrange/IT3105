import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sin,cos
 
         
def data_gen():
    gen_list = ([t,[np.cos(3*(t+np.pi/2))]] for t in np.arange(-1.2,0.6,0.01))
    return gen_list
 
 
def init():
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(-1.2, 1)
    return point
 
fig, ax = plt.subplots()
point, = ax.plot([0], [0], 'go')
point.set_data(0, 0)


def run(data):
 
    t, y = data
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
 
    if t >= xmax:
        ax.set_xlim(xmin, t)
        ax.figure.canvas.draw()
         
    if t <= xmin:
        ax.set_xlim(t, xmax)
        ax.figure.canvas.draw()
         
    if y >= ymax:
        ax.set_ylim(ymin, y)
        ax.figure.canvas.draw()
         
    if y <= ymin:
        ax.set_ylim(y, ymax)
        ax.figure.canvas.draw()
         
    point.set_data(t, y)
     
    return point


 
ani = animation.FuncAnimation(fig, run, data_gen, init_func=init,interval=10)
all_x = np.arange(-1.2,0.6,0.001)
all_y = np.cos(3*(all_x+np.pi/2))
plt.plot( all_x, all_y )

plt.show()
