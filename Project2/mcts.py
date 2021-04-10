from game import *
#from Tree import *
from copy import deepcopy
import random

class MCTS:




    def __init__(self, default_policy, exploration_constant, board):
        self.default_policy = default_policy
        self.exploration_constant = exploration_constant
        self.nodes = {}  # (state) --> node
        self.nodes[board.get_state()] = Node(board.get_player(), board.get_valid_actions())

    def init_MCT(self):
        self.nodes.clear()

    ## methods: Tree se
    def tree_search(self, time, board):
        while time:
            self.simulate(board) ## copy states
            time -= 1

        moves = board.get_move_distribution()
        root_node = self.nodes.get(board.get_state())
        distribution = np.zeros(len(moves))
        for index in range(len(distribution)):
            action = moves[index]
            if action not in root_node.values.keys():
                distribution[index] = 0
            else:
                distribution[index] = root_node.values[action][1]/root_node.N
        return distribution


    def simulate(self, board):
        board_copy = deepcopy(board)
        path = self.sim_tree(board_copy)         ##if test?
        z = self.sim_default(board_copy)
        self.backup(path, z)



    def sim_tree(self, board):
       # t = 0 dont think we need this. used in pseudocode to build trees
        state = board.get_state()
        action = self.select_move(board)
        path = []
        while not board.is_game_over(action):
            valid_actions = board.get_valid_actions()
            if state not in self.nodes.keys():
                node = Node( board.get_player(), valid_actions)
                #self.nodes.append(state, node)
                path.append(node)
                return path
            node = Node(board.get_player(), valid_actions)
            path.append(node)
            action = self.select_move(board)
            board.move(action)
            state = board.get_state()
        return path



    def sim_default(self, board):
        #TODO use policy to find move later
        #action = self.default_policy
        action = random.choice(board.get_valid_actions())
        winner = board.is_game_over(action)
        while len(board.get_valid_actions())>1:
            board.move(action)
            winner = board.is_game_over(action)
            #action = self.default_policy
            action = random.choice(board.get_valid_actions())

        return winner

    def select_move(self, board):
        valid_moves = board.get_valid_actions()
        player = board.get_player()
        action_values = []
        node = self.nodes.get(board.get_state())
        if not node:
            self.nodes[board.get_state()] = Node(board.get_state(), board.get_valid_actions())
            node = self.nodes[board.get_state()]
        for move in valid_moves:
            action_values.append(node.compute_value(move, self.exploration_constant, player))
        if player == 1:
            return valid_moves[np.argmax(action_values)]
        else:
            return valid_moves[np.argmin(action_values)]


    def backup(self, nodes, z): #nodes is a list of nodes representing the states, z is the end value
        
        for node in nodes:
            action = node.action
            node.update_state_visit()
            node.update_action_visit(action)
            node.update_value(action,z)



from math import sqrt, log
class Node:


    def __init__(self, player, valid_actions): #each node corresponds to a state
        self.N = 1
        self.action = None
        self.values = {}
        for action in valid_actions:
            self.values[action] =  [0,0] ## Q(s,a), N(s,a)

    def update_action_visit(self, action):
        if action not in self.values.keys():
            self.values[action] = [0,0]
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


import numpy as np
liste = [1,2,3,4]
liste2 = [5,6,7,8]

print(np.argmax(liste))