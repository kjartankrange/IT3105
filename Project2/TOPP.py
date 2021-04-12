from action_net import ANN 
from game import *
import random
import torch
class Turnament:

    def __init__(self, nets , board_size): #Nets should be a list
        self.nets = nets


        self.board_size = board_size
        self.results_table = {}
        for i in range(len(nets)):
            self.results_table[i+1] = 0

    
    def get_net_in_move(self,player_to_move):
        return self.player1 if player_to_move % 2 else self.player2

    def run_tournament(self):
        if not len(self.nets) >= 2:
            raise Exception(f"Tournament must have more than one player. There are now {len(self.nets)} players in the tournament")
    
        winner_matrix = [[0 for i in range(len(self.nets))] for j in range(len(self.nets))]
        for i in range(len(self.nets)):

            net1 = self.nets[i]
            for j in range(i + 1,len(self.nets)):
                net2 = self.nets[j]
                self.player1 = net1
                self.player2 = net2

                print(f"Player {i+1} is now playing player {j+1}")
                game = Game(self.board_size, 1)
                move = (2, 2)  # bogus move, this should be fixed generally, but crude solution works

                while not game.is_game_over(move):
                    move_index = self.get_net_in_move(game.get_player()).default_policy(game.get_state_and_player())
                    move = game.index_to_move(move_index)
                    game.move(move)
                winner = game.is_game_over(move)

                winner = 2 if winner == -1 else 1  # last round
                row = i if winner == 1 else j
                col = j if winner == 1 else i
                winner_matrix[row][col] += 1

                winner_index = i + 1 if winner == 1 else j + 1

                self.results_table[winner_index] += 1
                print(f"Player {winner_index} won" )
        game.visualise()
        return winner_matrix







    def show(self,graph=False):
        print("   Win statistics")
        print("{:>9} {:>9}\n".format( "Player", "Wins"))
        
        for key in self.results_table:
            print("{:>9} {:>9}".format( key, self.results_table[key]) )

if __name__ == "__main__":

    size = 4
    input_layer =  size**2
    learning_rate = 0.01
    
    hidden_layers = [16,16]
    output_layer = input_layer
    activation_function = "r" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
    optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
    M = "m"
    G = "g"  
    
    
    net1 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
    net1.load("cached nets/ann0.pt")
    
    net2 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
    net2.load("cached nets/ann5.pt")

    net3 = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
    net3.load("cached nets/ann28.pt")
    
    rounds = 1000
    round_interval = 50
    
    turnament = Turnament([net1, net2, net3], size)
    print(turnament.run_tournament())
    turnament.show()

