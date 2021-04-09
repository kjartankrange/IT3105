from game import *
from Tree import *

class MCTS:


    def __init__(self, default_policy, exploration_constant, tree, board):
        self.default_policy = default_policy
        self.exploration_constant = exploration_constant
        self.tree = tree
        self.board = board

    ## methods: Tree se
    def tree_search(self, starting_state, time):
        while time:
            self.simulate(self.board, starting_state) ## copy states
            time -= 1


    def simulate(self, board, starting_state):
        board.set_position(starting_state) ## implement in game
        path = self.sim_tree(board)         ##if test?
        z = self.sim_default(board)
        self.tree.backup(path,z)



    def sim_tree(self, board):
        t = 0
        state = board.get_state()
        action = self.tree.select_move(board, self.exploration_constant)
        path = []
        while not board.is_game_over(action):
            valid_actions = board.get_available_moves()
            if state not in self.tree.get_nodes():
                node = Node(state, board.get_player(), valid_actions)
                path.append(node)
                return path
            path.append(state)
            action = self.tree.select_move(board, self.exploration_constant)
            board.move(action)
            state = board.get_state()
        return path







    def sim_default(self, board):
        action = self.default_policy
        winner = board.is_game_over()
        while not winner:
            board.move(action)
            winner = board.is_game_over(action)
            action = self.default_policy
        return winner



class Tree:

    nodes = {} #( state) --> node


    def get_nodes(self):
        return self.nodes

    def select_move(self, board,  exploration_constant):
        valid_moves = board.get_available_moves()
        player = board.get_player()
        action_values = []
        node = self.nodes.get(board.get_state())

        for move in valid_moves:
            action_values.append(node.compute_value(move, exploration_constant, player))
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


    def __init__(self, state, player, valid_actions):
        N = 0
        self.action = None
        values = {}
        for action in valid_actions:
            values[action] =  [0,0] ## Q(s,a), N(s,a)

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
            return self.values[action][0] + exploration_constant * sqrt(log(self.N) / self.values[action][1])

        elif player == 2:
            return self.values[action][0] - exploration_constant * sqrt(log(self.N) / self.values[action][1])




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
