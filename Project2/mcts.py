from game import *
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
                #how much each action in a state is visited, on average
                distribution[index] = root_node.values[action][1]/(root_node.N if root_node.N!=0 else 1)
        return distribution

    #simulation, init and build tree
    def simulate(self, board):
        board_copy = deepcopy(board)
        path = self.sim_tree(board_copy)  #building tree
        if path and board_copy.get_valid_actions():
            z = self.sim_default(board_copy) #run default policy
            self.backup(path, z)


    #walk down montecarlo tree, add leafnode , return path
    def sim_tree(self, board):
        state = board.get_state()
        action = self.select_move(board) ## tree policy
        path = []

        while not board.is_game_over(action):
            valid_actions = board.get_valid_actions()
            
            #if new state, add leaf-node to tree
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


    #Rollout, from leaf node
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

    # Tree policy 
    def select_move(self, board):
        player = board.get_player()
        action_values = []
        node = self.nodes.get((board.get_state(), board.get_player()))
        valid_moves = list(node.values.keys())

        if not node:
            self.nodes[(board.get_state(), board.get_player())] = Node(board.get_state(), board.get_valid_actions())
            node = self.nodes[(board.get_state(), board.get_player())]

        for move in valid_moves:
            action_values.append(node.compute_value(move, self.exploration_constant, player))

        if player == 1:
            return valid_moves[np.argmax(action_values)] # p1 moves
        else:
            return valid_moves[np.argmin(action_values)] # opponent moves

    #Backpropagation
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

    #update value of action_visit in backprop
    def update_action_visit(self, action):
        self.values[action][1]  += 1

    #update value in backprop
    def update_value(self, action, z):
        q = self.values[action][0]
        self.values[action][0] += (z-q)/self.values[action][1]

    #node visited
    def update_state_visit(self):
        self.N += 1

    #set prev aciton
    def set_action(self, action):
        self.action = action

    #exploration constant determines how much value of node changes when visited
    def compute_value(self, action, exploration_constant, player):
        if player == 1:
            return self.values[action][0] + exploration_constant * sqrt(log(self.N if self.N > 0 else 1) / (self.values[action][1]+1)) # should we return zero or + by 1?

        elif player == 2:
            return self.values[action][0] - exploration_constant * sqrt(log(self.N if self.N > 0 else 1) / (self.values[action][1]+1)) # should we return zero or + by 1?



