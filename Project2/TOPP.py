from action_net import ANN 
from game import *
import random
import torch
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import glob



net_wins = 0
games = 0
class Tournament:
    

    def __init__(self, net1, net2,rounds, round_interval, board_size, counter,G):
        self.net1 = net1
        self.net2 = net2
        self.rounds = rounds
        self.round_interval = round_interval
        self.board_size = board_size
        self.results_table = {}
        self.counter = counter
        self.G = G

    
    def get_net_in_move(self,player_to_move):
        return self.net1 if player_to_move % 2 else self.net2

    def run(self, who_starts):
        results = [] #encode  information as a list of 1s and 2s

       
        games = [Game(self.board_size, who_starts ) for x in range(self.G) ] #Todo board takes in player
        
        for game in games: 
            move = (2,2) #bogus move, this should be fixed generally, but crude solution works

            
            while not game.is_game_over(move):
                
                if random.random()<0.8:
                    move_index = self.get_net_in_move(game.get_player()).default_policy(game.get_state_and_player())
                    move = game.index_to_move(move_index)
                else:
                    move_index = self.get_net_in_move(game.get_player()).stochastic_policy(game.get_state_and_player())
                    move = game.index_to_move(move_index)
                #move = random.choice(game.get_valid_actions())
                
                game.move(move)
                
            winner = game.is_game_over(move)
            winner = 2 if winner == -1 else 1 #last round
            results.append(winner)
            self.counter.net_wins += 1 if winner == 1 else 0
            self.counter.games +=1
        #game.visualise()
        #register winners at each round
        #self.results_table[round_] = (results.count(1),results.count(2))

            
    
            
    def show(self,graph=False):
        print("        Winners of Tournament")
        print("{:>9} {:>9} {:>9}\n".format("round", "net1", "net2"))
        
        for key in self.results_table:
            print("{:>9} {:>9} {:>9}".format(key,self.results_table[key][0], self.results_table[key][1]) ) 

class Counter:
    def __init__(self):
        self.net_wins = 0
        self.games = 0

def round_robin(nets, G, interval,name_of_simulation,DEMO_LOADER):
    for j in range(1,nets,interval):
        size = 4
        input_layer =  size**2
        learning_rate = 0.001
        
        hidden_layers = [128,64]
        output_layer = input_layer
        activation_function = "r" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
        optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
        M = "m"

        counter = Counter() 
        """
        net1 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
        net1.load(f"cached nets/testingann{j}_lf=b.pt")
        """
        net1 = net_loader(name_of_simulation,j,DEMO_LOADER)

        for i in range(1,nets,interval):
            if i == j:
                continue
            """
            net2 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
            net2.load(f"cached nets/testingann{i}_lf=b.pt")
            """
            net2 = net_loader(name_of_simulation,i,DEMO_LOADER)
            rounds = 1
            round_interval = 1
            tournament = Tournament(net1, net2,rounds, round_interval, size, counter, G)
            tournament.run(1)
            #Tournament.show()
        print(f"NET {j} WON {counter.net_wins} out of {counter.games}")
        for q in range(counter.net_wins):
            resultinglist.append(j)
    plt.hist(resultinglist, bins=int((nets-1)/interval)+1) #[0,10,20,30,40,50,60,70,80]
    plt.show()


def net_loader(name_of_simulation,i,DEMO_LOADER):
    if DEMO_LOADER: 
        
        size = 4
        number_actual_games = 100
        input_layer =  size**2
        learning_rate = 0.001
        
        hidden_layers = [128,64]
        output_layer = input_layer
        activation_function = "r" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
        optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
        M = number_actual_games
        net = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G="")
        net.load(f"{pathlib.Path(__file__).parent.absolute()}/demo nets/testingann{i}_lf=b.pt")  
        return net    
        
    folder_name, name_of_simulation =  name_of_simulation.split(":")
    file_name = glob.glob(f"{pathlib.Path(__file__).parent.absolute()}/{folder_name}/{name_of_simulation}:{i}*")[0]
    
    with open(file_name, "r") as f:
        
        meta_data = file_name.split(":")[2].split("_")
        learning_rate = float(meta_data[0])
        input_layer = int(meta_data[1])
        hidden_layers = []
        for layer in meta_data[2][1:-1].split(","):
            hidden_layers.append(int(layer))
        output_layer = int(meta_data[3])
        activation_function = meta_data[4]
        optimizer = meta_data[5]
        loss_function = meta_data[6].split(".")[0]
    
    
    M = "m"
    g = "g"
    net = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,g,loss_function)
    net.load(file_name)

    return net



if __name__ == "__main__":
    resultinglist = []
    nets = 84
    interval = 1
    G = 1 #number of games between any two agents
    folder_to_load = "cached nets/"
    name_of_simulation = "dette_er_demo"
    
    DEMO_LOADER = True #Set to true too run pretrained simulation in demo nets
    if DEMO_LOADER:
        #set variablene over inn her @audun og kjør sånn at når demo_loader er true så bare får vi riktig

    file_location = folder_to_load + ":" + name_of_simulation

    round_robin(nets, G, interval,file_location,DEMO_LOADER)
