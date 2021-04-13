from action_net import ANN 
from game import *
import random
import torch
net_wins = 0
games = 0
class Turnament:
    

    def __init__(self, net1, net2,rounds, round_interval, board_size):
        self.net1 = net1
        self.net2 = net2
        self.rounds = rounds
        self.round_interval = round_interval
        self.board_size = board_size
        self.results_table = {}

    
    def get_net_in_move(self,player_to_move):
        return net1 if player_to_move % 2 else net2

    def run(self, who_starts):
        results = [] #encode  information as a list of 1s and 2s

        for round_ in range(self.round_interval,self.rounds+self.round_interval,self.round_interval):
            games = [Game(self.board_size, who_starts ) for x in range(self.round_interval) ] #Todo board takes in player
            
            for game in games: 
                move = (2,2) #bogus move, this should be fixed generally, but crude solution works
    
                
                while not game.is_game_over(move):
                    
                    move_index = self.get_net_in_move(game.get_player()).default_policy(game.get_state_and_player())
                    move = game.index_to_move(move_index)
                    
                    #move = random.choice(game.get_valid_actions())
                    
                    game.move(move)
                    
                winner = game.is_game_over(move)
                winner = 2 if winner == -1 else 1 #last round
                results.append(winner)
                counter.net_wins += 1 if winner == 1 else 0
                counter.games +=1
            #game.visualise()
            #register winners at each round
            self.results_table[round_] = (results.count(1),results.count(2))

            
    
            
    def show(self,graph=False):
        print("        Winners of turnament")
        print("{:>9} {:>9} {:>9}\n".format("round", "net1", "net2"))
        
        for key in self.results_table:
            print("{:>9} {:>9} {:>9}".format(key,self.results_table[key][0], self.results_table[key][1]) ) 

class Counter:
    def __init__(self):
        self.net_wins = 0
        self.games = 0

if __name__ == "__main__":

    for j in range(0,10):
        size = 4
        input_layer =  size**2
        learning_rate = 0.01
        
        hidden_layers = [16,16]
        output_layer = input_layer
        activation_function = "r" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
        optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
        M = "m"
        G = "g" 

        counter = Counter() 

        for start in range(1,3):
            net1 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
            net1.load(f"cached nets/ann{j}audun_size4.pt")
            for i in range(0,10):
                net2 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
                net2.load(f"cached nets/ann{i}.pt")
                rounds = 1
                round_interval = 1
                who_starts = start
                turnament = Turnament(net1, net2,rounds, round_interval, size)
                turnament.run(who_starts)
                #turnament.show()
        print(f"NET {j} WON {counter.net_wins} out of {counter.games}")