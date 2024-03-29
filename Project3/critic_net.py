import numpy as np
import pdb
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
import random
import pathlib

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

class Critic_net(nn.Module):
    
    def __init__(self,learning_rate, input_layer, hidden_layers, output_layer, activation_function, optimizer, M, G,loss_function="b"):
        super(Critic_net,self).__init__()
        self.learning_rate = learning_rate
        self.activation_function = activation_function
        self.M = M
        self.G = G
        self.losses = []
        
        
        #now set layers
        layers = []
        if len(hidden_layers) == 0:
            layers.append(nn.Linear(input_layer,output_layer))
          
        else:     
            layers.append(nn.Linear(input_layer+1,hidden_layers[0]))
            layers.append(self.get_torch_activation_function(activation_function))
            for i in range(len(hidden_layers)-1):
                layers.append( nn.Linear(hidden_layers[i], hidden_layers[i+1]) )
                layers.append(self.get_torch_activation_function(activation_function))
            layers.append(nn.Linear(hidden_layers[-1] if len(hidden_layers) != 0 else input_layer,output_layer) )
        #what should dim be, do we need a dim? 
        layers.append(nn.Linear(output_layer,1))
        
        #String for loading net later
        self.save_string = f"{learning_rate}_{input_layer}_{hidden_layers}_{output_layer}_{activation_function}_{optimizer}_{loss_function}.pt"
        
        self.model = nn.Sequential( *layers )
        self.optimizer = self.set_optimizer(optimizer)
        
        #We have used binary cross entropy ass it seemed most fitting, chosen as it is quicker to differentiate than sigmoid
        #Alo it is recommended on the web for cases similar to this like this one 
       
        if loss_function.lower() in ["me","m"]:
            self.loss = torch.nn.MSELoss()
            self.loss_function = "m"
        else:
            self.loss = torch.nn.KLDivLoss(reduction="batchmean")
            self.loss_function = "KLD"
        
   
    
    #only function needed to implement from superclass Module
    def forward(self,state, action):
              
        input_tensor = torch.FloatTensor(state + [action])
        with torch.no_grad():
            return self.model(input_tensor)
   
    #input data [state, distribution over possible moves sum(moves) = 1] 
    def fit(self,s_a_tup, sp_ap_tup, reward, gamma):
        
        self.model.train() #Do we need to add this?
        state, action = s_a_tup
        state_p, action_p = sp_ap_tup
        
        
        self.optimizer.zero_grad()

        prediction = self.model(torch.FloatTensor(state + [action]))
        
        target = self.model(torch.FloatTensor(state_p + [action_p]))
        

        

        #this should be mean_sq_error
        loss = self.loss(prediction, target*gamma + reward) 
        
        
        loss.backward()
        self.optimizer.step()

        self.losses.append(loss.item())
        self.model.train(False)
        if reward==0 or reward==-100:
            print(sum(self.losses)/len(self.losses),"loss",prediction.item(),"pred", target.item()+reward,"target")
        return loss.item() 

    #returns index of greedy recommended move
    def default_policy(self,state):
        mask = [0 if char != "0" else 1 for char in state][1:]
        mask = torch.FloatTensor(mask)

        return torch.argmax(self.forward(state)*mask).item()

    #return index of a move stochastically recommended
    def stochastic_policy(self,state):
        stochastic_probabilities = self.forward(state).tolist()
        mask = [0 if char != "0" else 1 for char in state[1:]]
        mask = torch.FloatTensor(mask)
        stoch_probs_legal = self.forward(state)*mask
        stoch_probs_legal = stoch_probs_legal/torch.sum(stoch_probs_legal)
        indecies = [x for x in range(len(stochastic_probabilities))]
        #TODO NORMALIZE RESULTS IN Forward? like should have been done in defualt  pol
        #print(len(indecies))
        #print(len(stochastic_probabilities))
        #print(stoch_probs_legal)
        #print(random.choices(indecies,stoch_probs_legal,k=1), "choice")
        return random.choices(indecies,stoch_probs_legal.tolist(),k=1)[0]
    
    #This function is where the learning rate is relevant    
    def set_optimizer(self, optimizer):
        if optimizer in ["Adagrad","ag"]:
            return torch.optim.Adagrad(list(self.model.parameters()), lr=self.learning_rate,lr_decay=0.05)
        elif optimizer in ["SGD","s"]:
            return torch.optim.SGD(list(self.model.parameters()), lr=self.learning_rate)
        elif optimizer in ["RMSprop","r"]:
            return torch.optim.RMSprop(list(self.model.parameters()), lr=self.learning_rate)
        elif optimizer in ["Adam","ad"]:
            return torch.optim.Adam(list(self.model.parameters()), lr=self.learning_rate)
        else:
            raise Exception("Invalid Optimizer")

    #used to transelate between strings and Pytorch implementations 
    def get_torch_activation_function(self, activation_function):
        if activation_function in ["linear", "l"]:
            return None
        elif activation_function in ["sigmoid","s"]:
            return nn.Sigmoid()
        elif activation_function in ["tanh","t"] :
            return nn.Tanh()
        elif activation_function in ["RELU", "r"]:
            return nn.ReLU()
        else:
            raise Exception("Invalid Activation Function")
    
    def _string_to_number_tensor(self,string):
        lst = []
        for char in string:
            lst.append(int(char))
        return torch.FloatTensor(lst)
    
    def save(self,name_of_simul,iteration):                
        torch.save(self.state_dict(), f"{pathlib.Path(__file__).parent.absolute()}/demo nets/{name_of_simul}:{iteration}:{self.save_string}")
    
    def load(self,path):
        self.load_state_dict(torch.load(path))

if __name__ == "__main__":
    learning_rate = 0.2
    input_layer = 4*4
    hidden_layers = [30,50]
    output_layer = input_layer
    activation_function = "s" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
    optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
    M = "m"
    G = "g"    


   
    my_net = Critic_net(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)