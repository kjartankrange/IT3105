
from mcts import MCTS
from game import Game
import numpy as np
from tqdm import tqdm
import random

class RL:
    

    def __init__(self, save_interval, NN,MCTS,  number_actual_games, starting_board_state,number_search_games, player_to_start, size):
        self.save_interval = save_interval
        self.number_actual_games = number_actual_games
        self.starting_board_state = starting_board_state
        self.number_search_games = number_search_games
        self.player = player_to_start
        self.size = size


        self.MCTS = MCTS
        self.game = starting_board_state
        self.NN = NN

    def RL_algorhitm(self):
        
        save_interval = self.save_interval # set save interval for saving anet

        replay_buffer = {} # Clear Replay Buffer (RBUF)

        #self.NN.save() #Randomly initialize parameters (weights and biases) of ANET


        for g_a in tqdm(range(self.number_actual_games)):
            #TODO skal vi lage nye games eller resete?    
            self.game = Game(self.size, self.player) # Initialize the actual game board (Ba) to an empty board.

            starting_board_state = self.starting_board_state # s_init ← starting board state

            #TODO Spør mattias hvordan dette funker
            #self.MCTS.init_tree() # Initialize the Monte Carlo Tree (MCT) to a single root, which represents sinit

            is_game_over = False
            while not is_game_over: # While Ba not in a final state:
                """
                MCTS.board = starting_board_state # Initialize Monte Carlo game board (Bmc) to same state as root.
                
                for g_s in range(self.number_search_games):
                    
                    – Use tree policy Pt to search from root to a leaf (L) of MCT. Update Bmc with each move.
                    – Use ANET to choose rollout actions from L to a final state (F). Update Bmc with each move. 
                    – Perform MCTS backpropagation from F to root.
                    
                # next gs
                """
                D = [] # distribution of visit counts in MCT along all arcs emanating from root.

                #D = self.MCTS.tree_search(B_a, self.number_search_games) #TODO denne returnerer ingenting atm

                #replay_buffer[root] = D # Add case (root, D) to RBUF

                move = random.choice(self.game.get_valid_actions()) #self.game.get_valid_actions()[argmax(replay_buffer[root])] # Choose actual move (a*) based on D

                if self.game.is_game_over(move):
                    is_game_over = True
                    break
                self.game.move(move) # Perform a* on root to produce successor state s*
                
                s = self.game.get_board()

                B_a = s    # Update Ba to s*

                #In MCT, retain subtree rooted at s*; discard everything else.

                root = s # root←s*
                self.game.visualise()

            # Train ANET on a random minibatch of cases from RBUF
            """
            training_cases = random.sample(self.buffer, min(len(self.buffer),self.batch_size))
            x_train, y_train = list(zip(*training_cases))
            loss, acc = self.ANN.fit(x_train, y_train)
            self.losses.append(loss)
            self.accuracies.append(acc)
            """
            #Save ANETS parameters
            """    
            if (g_a+1) % save_interval == 0:
                #TODO how to do this? # Save ANET’s current parameters for later use in tournament play.
            """ 

if __name__ == "__main__":
    NN = 0
    player = 1
    size = 5
    MCTS = 0
    run = RL(100,NN,MCTS, 0, Game(size,player),1,player, size)
    run.RL_algorhitm()



