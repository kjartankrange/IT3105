import numpy as np
import pdb
import torch
import torch.nn as nn
import torch.nn.functional as F

"""

• In the ANET, the learning rate, the number of hidden layers and neurons per layer, 
    along with any of the following activation functions for hidden nodes: linear, sigmoid, tanh, RELU.
• The optimizer in the ANET, with (at least) the following options all available: 
    Adagrad, Stochastic Gradient Descent (SGD), RMSProp, and Adam.
• The number (M) of ANETs to be cached in preparation for a TOPP. These should be cached, 
starting with an untrained net prior to episode 1, at a fixed interval throughout the training episodes.
• The number of games, G, to be played between any two ANET-based agents
 that meet during the round-robin play of the TOPP.
"""


class NN:
    def __init__(self, learning_rate, hidden_layers, M, G, optimizer, activation_function, input_layer_size, epochs):
        self.learning_rate = learning_rate
        self.hidden_layers = hidden_layers
        self.input_layer_size = input_layer_size
        self.M_ANETS_cached = M
        self.num_of_games = G
        self.epochs = epochs

        self.configure(activation_function, optimizer)

    def configure(self, activation_function, optimizer):
        self.activation_function = self.set_activation_function(activation_function) #linear, sigmoid, tanh, RELU
        layers = [torch.nn.Linear(self.input_layer_size+1,self.hidden_layers[0])]
        layers.append(activation_function) if activation_function != None else None
        for i in range(len(self.hidden_layers)-1):
            layers.append(torch.nn.Linear(self.hidden_layers[i], self.hidden_layers[i+1]))
            layers.append(activation_function) if activation_function != None else None
        layers.append(torch.nn.Linear(self.hidden_layers[-1],self.input_layer_size))
        layers.append(torch.nn.Softmax(dim=-1))
        self.model = torch.nn.Sequential(*layers)
        self.loss_fn = torch.nn.BCELoss(reduction="mean")
        self.optimizer = self.set_optimizer(self.optimizer) #Adagrad, Stochastic Gradient Descent (SGD), RMSProp, and Adam
    
    def fit(self, input_data, target):
        #Transform data into tensors (needed format)
        x = torch.Tensor(input_data)
        y = torch.Tensor(input_data)
        for i in range(self.epochs):
            pred_y = self.model(x)
            loss = self.loss_fn(pred_y, y)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        acc = pred_y.argmax(dim=1).eq(y.argmax(dim=1)).sum().numpy()/len(y)
        return loss.item(), acc 

    def get_move(self, board):
        legal = board.get_legal_actions()
        factor = [1 if move in legal else 0 for move in board.all_moves]
        input_data = torch.Tensor(board.flat_state)
        with torch.no_grad():
            probs = self.model(input_data).data.numpy()
        sum = 0
        new_probs = np.zeros(board.size ** 2)
        for i in range(board.size ** 2):
            if factor[i]:
                sum += probs[i]
                new_probs[i] = probs[i]
            else:
                new_probs[i] = 0
        new_probs /= sum
        indices = np.arange(board.size ** 2)
        stoch_index = np.random.choice(indices, p=new_probs)
        greedy_index = np.argmax(new_probs)
        return new_probs, stoch_index, greedy_index



    def set_optimizer(self, optimizer):
        if optimizer=="Adagrad":
            return torch.optim.Adagrad(list(self.model.parameters()), lr=self.learning_rate)
        elif optimizer == "SGD":
            return torch.optim.SGD(list(self.model.parameters()), lr=self.learning_rate)
        elif optimizer == "RMSprop":
            return torch.optim.RMSprop(list(self.model.parameters()), lr=self.learning_rate)
        elif optimizer == "Adam":
            return torch.optim.Adam(list(self.model.parameters()), lr=self.learning_rate)
        else:
            raise Exception("Invalid Optimizer")

    def set_activation_function(self, activation_function):
        if activation_function == "linear":
            return None
        elif activation_function == "sigmoid":
            return torch.nn.Sigmoid()
        elif activation_function == "tanh":
            return torch.nn.Tanh()
        elif activation_function == "RELU":
            return torch.nn.ReLU()
        else:
            raise Exception("Invalid Activation Function")

#Get this to work
"""
    def save(self, size, level):
        torch.save(self.state_dict(), "models/{}_ANN_level_{}".format(size,level))
        print("\nModel has been saved to models/{}_ANN_level_{}".format(size,level))

    def load(self, size, level):
        self.load_state_dict(torch.load("models/{}_ANN_level_{}".format(size,level)))
        print("Loaded model from models/{}_ANN_level_{}".format(size,level))
"""