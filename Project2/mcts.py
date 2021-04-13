from game import *
#from Tree import *
from copy import deepcopy
import random
import numpy as np

class MCTS:




    def __init__(self, default_policy, exploration_constant, board,eps):
        self.default_policy = default_policy
        self.exploration_constant = exploration_constant
        self.nodes = {}  # (state, player) --> node
        self.nodes[(board.get_state(), board.get_player())] = Node(board.get_player(), board.get_valid_actions())
        self.eps = eps

    def init_MCT(self):
        self.nodes.clear()

    ## methods: Tree search
    def tree_search(self, time, board):
        while time:
            self.simulate(board) #run one iteration
            time -= 1

        moves = board.get_move_distribution()
        root_node = self.nodes.get((board.get_state(), board.get_player()))

        #find distribution
        distribution = np.zeros(len(moves))
        for index in range(len(distribution)):
            action = moves[index]
            if action not in root_node.values.keys():
                distribution[index] = 0
            else:
                distribution[index] = root_node.values[action][1]/(root_node.N if root_node.N!=0 else 1)
        return distribution

    #simulation
    def simulate(self, board):
        board_copy = deepcopy(board)
        path = self.sim_tree(board_copy)  #building tree
        if path and board_copy.get_valid_actions():
            z = self.sim_default(board_copy) #run default policy
            self.backup(path, z)
            #print(path)


    #walk down montecarlo tree , return path
    def sim_tree(self, board):
        state = board.get_state()
        action = self.select_move(board) ## tree policy
        path = []

        while not board.is_game_over(action):
            valid_actions = board.get_valid_actions()
            if (state, board.get_player()) not in self.nodes.keys():
                node = Node(board.get_player(), valid_actions)
                self.nodes[(state, board.get_player())] = node
                return path
            node = self.nodes.get((state, board.get_player()))
            path.append(node)
            action = self.select_move(board)
            node.set_action(action)
            board.move(action)
            state = board.get_state()

        return path


    #Rollout
    def sim_default(self, board): 
        move = random.choice(board.get_valid_actions())
        while (not board.is_game_over(move)):
            if not board.get_valid_actions():
                break
            if random.random() < self.eps:
                move = random.choice(board.get_valid_actions())
            else:
                move_index = self.default_policy.stochastic_policy(board.get_state_and_player())
                move = board.index_to_move(move_index)
            
            board.move(move)
        return board.is_game_over(move) ## returns the winner, 1 for player 1, 2 for player 2.


    def select_move(self, board):
        valid_moves = board.get_valid_actions()
        player = board.get_player()
        action_values = []
        node = self.nodes.get((board.get_state(), board.get_player()))
        if not node:
            self.nodes[(board.get_state(), board.get_player())] = Node(board.get_state(), board.get_valid_actions())
            node = self.nodes[(board.get_state(), board.get_player())]

        for move in valid_moves:
            action_values.append(node.compute_value(move, self.exploration_constant, player))
        if player == 1:
            return valid_moves[np.argmax(action_values)]
        else:
            return valid_moves[np.argmin(action_values)]


    def backup(self, nodes, z): #nodes is a list of nodes representing the states, z is the end value
        
        for node in nodes: #node.action is prev action
            action = node.action
            node.update_state_visit()
            node.update_action_visit(action)
            node.update_value(action,z)



from math import sqrt, log
class Node:


    def __init__(self, player, valid_actions): #each node corresponds to a state
        self.N = 0
        self.action = None
        self.values = {}
        for action in valid_actions:
            self.values[action] =  [0,0] ## Q(s,a), N(s,a)

    def update_action_visit(self, action):
        self.values[action][1]  += 1

    def update_value(self, action, z):
        q = self.values[action][0]
        self.values[action][0] += (z-q)/self.values[action][1]

    def update_state_visit(self):
        self.N += 1

    def set_action(self, action):
        self.action = action

    def compute_value(self, action, exploration_constant, player):
        if player == 1:
            return self.values[action][0] + exploration_constant * sqrt(log(self.N if self.N > 0 else 1) / (self.values[action][1]+1)) # should we return zero or + by 1?

        elif player == 2:
            return self.values[action][0] - exploration_constant * sqrt(log(self.N if self.N > 0 else 1) / (self.values[action][1]+1)) # should we return zero or + by 1?




    ## Needs list of children
    ## needs q and n (q being the accumulated scores of visiting this node, n the number of visits)
    ## needs add children
    ## needs move taken as an attribute
    ## score, if it is a leaf node (i.e representing an end state of the board)
    ## what about the exploration constant??
    ## parent?


if __name__ == "__main__":
    game = Game(5, 1)
    from action_net import ANN
    learning_rate = 0.2
    input_layer = 4*4
    hidden_layers = [30,50]
    output_layer = input_layer
    activation_function = "s" #choices: "linear" OR "l", "sigmoid" OR "s", "tanh" OR "t", "RELU" OR "r"
    optimizer = "ad" #choices: ["Adagrad","ag"], ["SGD","s"]:["RMSprop","r"]:["Adam","ad"]:
    M = "m"
    G = "g"       
    my_net = ANN(learning_rate,input_layer,hidden_layers,output_layer,activation_function,optimizer,M,G)
    mcts = MCTS(ny_net, 1.4, game)
