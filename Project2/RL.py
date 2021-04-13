
from mcts import MCTS
from game import Game
import numpy as np
from tqdm import tqdm
import random
from action_net import ANN


class RL:
    

    def __init__(self, save_interval, model, montecarlo,  number_actual_games, starting_board_state,number_search_games, player_to_start, size, batch_size,batch_size_delta, eps):
        self.save_interval = save_interval
        self.number_actual_games = number_actual_games
        self.starting_board_state = starting_board_state
        self.number_search_games = number_search_games
        self.player = player_to_start
        self.size = size
        self.batch_size = batch_size

        self.eps = eps
        self.MCTS = montecarlo
        self.game = starting_board_state
        self.model = model
        self.batch_size_delta = batch_size_delta

    def RL_algorhitm(self):
        
        save_interval = self.save_interval # set save interval for saving anet

        replay_buffer = {} # Clear Replay Buffer (RBUF)

        #self.NN.save() #Randomly initialize parameters (weights and biases) of ANET
        p1 = 0

        for g_a in tqdm(range(self.number_actual_games)):
            #TODO skal vi lage nye games eller resete?    
            self.game = Game(self.size, self.player) # Initialize the actual game board (Ba) to an empty board.

            starting_board_state = self.starting_board_state # s_init ← starting board state

            #self.MCTS.init_MCT() # Initialize the Monte Carlo Tree (MCT) to a single root, which represents sinit
            self.MCTS = MCTS(self.model, exploration_constant, self.game, self.eps)

            is_game_over = False
            B_a = self.game.get_state_and_player()
            root = B_a
            move = (2,2)
            while not self.game.is_game_over(move): # While Ba not in a final state:
                """
                MCTS.board = starting_board_state # Initialize Monte Carlo game board (Bmc) to same state as root.
                
                for g_s in range(self.number_search_games):
                    
                    – Use tree policy Pt to search from root to a leaf (L) of MCT. Update Bmc with each move.
                    – Use ANET to choose rollout actions from L to a final state (F). Update Bmc with each move. 
                    – Perform MCTS backpropagation from F to root.
                    
                # next gs
                """
                D = [] # distribution of visit counts in MCT along all arcs emanating from root.

                D = self.MCTS.tree_search(self.number_search_games, self.game) #TODO denne returnerer ingenting atm
            
                replay_buffer[root] = D # Add case (root, D) to RBUF

                #move = random.choice(self.game.get_valid_actions()) #self.game.get_valid_actions()[argmax(replay_buffer[root])] # Choose actual move (a*) based on D
                move = self.game.get_move_distribution()[np.argmax(replay_buffer[root])]
               
                #self.game.visualise()
                self.game.move(move) # Perform a* on root to produce successor state s*
                
                s = self.game.get_state_and_player()

                B_a = s    # Update Ba to s*

                #In MCT, retain subtree rooted at s*; discard everything else.

                root = s # root←s*
                #self.game.visualise()
            if self.game.is_game_over(move)==1:
                p1+=1
            # Train ANET on a random minibatch of cases from RBUF
            self.eps *=0.95
            if g_a== 0:
                self.model.save(g_a)
                self.batch_size+=self.batch_size_delta
            training_tuples = []
            sample_keys = random.sample(replay_buffer.keys(), min(len(replay_buffer.keys()),self.batch_size))
            for key in sample_keys:
                training_tuples.append((key,replay_buffer[key]))
            loss, accuracy = self.model.fit(training_tuples)  
            print(f"loss: {loss}")
            print(f"accuracy {accuracy}")
            print(f"p1 won {p1} out of {g_a}")
            #Save ANETS parameters
            
            if (g_a+1) % save_interval == 0:
                self.model.save(g_a)
                self.batch_size+=self.batch_size_delta
                #TODO how to do this? # Save ANET’s current parameters for later use in tournament play.
            

if __name__ == "__main__":
   
    
    player = 1
    size = 4
    input_layer =  size**2
    learning_rate = 0.01
    
    hidden_layers = [16,16]
    output_layer = input_layer
    activation_function = "s" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
    optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
    M = "m"
    G = "g"       
    my_net = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
    batch_size = 100
    batch_size_delta = 100
    default_policy = None
    exploration_constant = 1
    board = Game(size, player)
    number_search_games = 1000
    number_actual_games = 30
    save_interval = 1
    eps = 1
    montecarlo = MCTS(my_net, exploration_constant, board, eps)
    run = RL(save_interval,my_net,montecarlo, number_actual_games, board,number_search_games,player, size, batch_size, batch_size_delta, eps)
    run.RL_algorhitm()



