import torch
import torch.nn as nn
import torch.nn.functional as F
from random import *


class TableCritic():
    
    def __init__(learning_rate, discount_factor, trace_decay_factor):
        return
        
    def train(starting_state):
        values = {starting_board: random.random()*0.1}
        moves = starting_state.get_available_moves()
        policy = {}
        for move in moves:
            policy[(move, starting_state)] = 0


        
        

