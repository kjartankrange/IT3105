
from mcts import MCTS
from game import Game
import numpy as np
from tqdm import tqdm
import random
from action_net import ANN
import matplotlib.pyplot as plt

class RL:
    

    def __init__(self, save_interval, model, montecarlo,  number_actual_games, starting_board_state,number_search_games, player_to_start, size, batch_size,batch_size_delta, eps, eps_delta,save_file, visualise, name_of_simulation):
        self.save_interval = save_interval
        self.number_actual_games = number_actual_games
        self.starting_board_state = starting_board_state
        self.number_search_games = number_search_games
        self.player = player_to_start
        self.size = size
        self.batch_size = batch_size

        self.eps = eps
        self.eps_delta = eps_delta
        self.MCTS = montecarlo
        self.game = starting_board_state
        self.model = model
        self.batch_size_delta = batch_size_delta
        self.save_file = save_file
        self.visualise = visualise
        self.name_of_simulation = name_of_simulation

    def RL_algorhitm(self):
        
        save_interval = self.save_interval # set save interval for saving anet

        replay_buffer = {} # Clear Replay Buffer (RBUF)

        #Randomly initialize parameters (weights and biases) of ANET, done later but before train

        p1 = 0 # counter of how many wins player 1 has

        for g_a in tqdm(range(self.number_actual_games)):

            self.game = Game(self.size, self.player) # Initialize the actual game board (Ba) to an empty board.

            # Initialize the Monte Carlo Tree (MCT) to a single root, which represents sinit
            self.MCTS = MCTS(self.model, exploration_constant, self.game, self.eps)

            B_a = self.game.get_state_and_player() # save state

            root = B_a #save state in root, for RBUF

            move = random.choice(self.game.get_valid_actions()) #bogus move, needed because is_game_over takes in a move
            while not self.game.is_game_over(move): # While Ba not in a final state:

                D = [] # distribution of visit counts in MCT along all arcs emanating from root.

                D = self.MCTS.tree_search(self.number_search_games, self.game) # find distribution of moves played in MCTS
            
                replay_buffer[root] = D # Add case (root, D) to RBUF

                # Choose actual move (a*) based on D
                move = self.game.get_move_distribution()[np.argmax(replay_buffer[root])]
               
                #self.game.visualise()
                self.game.move(move) # Perform a* on root to produce successor state s*

                #if visualising
                if self.visualise:
                    self.game.visualise(True)
                
                s = self.game.get_state_and_player() # set state to s 

                B_a = s    # Update Ba to s*

                #In MCT, retain subtree rooted at s*; discard everything else.

                root = s # root←s*
                
                #self.game.visualise()
            if self.game.is_game_over(move)==1:
                p1+=1
                if visualise:
                    self.game.visualise(True)


            self.eps *=self.eps_delta # lower delta

            #save untrained net
            if g_a== 0:
                self.model.save(self.name_of_simulation,0)
                self.batch_size+=self.batch_size_delta
            
            # Train ANET on a random minibatch of cases from RBUF
            training_tuples = []
            sample_keys = random.sample(replay_buffer.keys(), min(len(replay_buffer.keys()),self.batch_size))
            for key in sample_keys:
                training_tuples.append((key,replay_buffer[key]))
            loss, accuracy = self.model.fit(training_tuples)  

            print(f"loss: {loss}")
            print(f"accuracy {accuracy}")
            print(f"p1 won {p1} out of {g_a+1}")

            if self.save_file: #save loss and accuracy
                with open("data.txt","a") as f:
                    f.write(f"{loss},{accuracy}\n")

            #Save ANET
            
            if (g_a+1) % save_interval == 0:
                self.model.save(self.name_of_simulation,g_a+1)
                self.batch_size+=self.batch_size_delta
            


if __name__ == "__main__":
   
    #Game
    player = 1 
    size = 4 # size of board from 3-10
    number_actual_games = 200 # episodes / epochs
    
    #ANN
    input_layer =  size**2 
    learning_rate = 0.001 # learning rate in NN
    hidden_layers = [128,64] # gives size of net and num of neurons
    output_layer = input_layer
    activation_function = "r" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
    optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
    M = number_actual_games # how many games to save?
    save_interval = number_actual_games/M # how often save?
    my_net = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G="")
    
    #MCTS
    batch_size = 500 # batch size sent to NN
    batch_size_delta = 0 # change in batch size
    exploration_constant = 1 # needed in mcts, how much values change when node action visited
    board = Game(size, player) 
    number_search_games = 500 # games in montecarlo
    eps = 0.9 # starting delta, if 1 => all moves random in mcts rolloiut
    eps_delta = 0.99 #change in delta

    record_training = False # record acc and loss

    name_of_simulation = "audun" #do not use ":" as part of name
    visualise = False # show moves during actual games
    
    montecarlo = MCTS(my_net, exploration_constant, board, eps)
    run = RL(save_interval,my_net,montecarlo, number_actual_games, board,number_search_games,player, size, batch_size, batch_size_delta, eps, eps_delta, record_training, visualise, name_of_simulation)
    run.RL_algorhitm()





