

from node import *
import copy
from node import *
from Visualisation import *


def make_triangle(size):  # Helperfunction for creating triangles.
    lst = []
    node_counter = 1
    for i in range(1, size + 1):
        row = []
        for j in range(i):
            row.append(Node(1, node_counter))
            node_counter += 1
        lst.append(row)
    return lst


class Board:
    opposite_directions = {"NE": "SW", "NW": "SE", "SW": "NE", "SE": "NW", "E": "W",
                           "W": "E"}  # a mapping of of opposite directions in order to get correct moves from neighbours' neighbours.

    ## del opp i hjelpefunksjoner: make_board(), set_neighbours, set_doubleneighbours()
    def __init__(self, shape, size,
                 dead_pos_touples):  # initialise the board with shape, size and boardpositions without a peg.
        self.board = []
        self.node_count = 0
        self.size = size

        if shape == "t" and (size not in range(4, 9)) or shape == "d" and (size not in range(3, 7)):
            raise Exception("wrong initialization")  # the board must be of correct dimensions.
        self.shape = shape
        # TODO: Create helper functions in order to make the code more segmented.
        if shape == "t":  # make the triangle board.
            self.shape = shape
            self.board = make_triangle(size)

        elif shape == "d":  # make the diamond board.
            lst = make_triangle(size)
            counter = sum(len(row) for row in lst) + 1
            for i in range(size - 1, 0, -1):
                row = []
                for j in range(i):
                    row.append(Node(1, counter))
                    counter += 1
                lst.append(row)
            self.board = lst

            # lst.append(make_triangle(size)[:-1][::-1]) #trim of mid part and flip list on head
        # Øking: NW = [i-1,j-1] NE = [i-1,j] W = [i,j-1] E =[i,j+1] SW = [i+1,j] SE = [i+1,j+1]
        # Minking NW = [i-1,j] NE = [i-1,j+1] W = [i,j-1] E =[i,j+1] SW = [i+1,j-1] SE = [i+1,j]

        # update the the node count, representing the number of nodes with pegs.
        for lst in self.board:
            for node in lst:
                self.node_count += 1
        # Add padding
        board_copy = []
        for lst in self.board:
            row = []
            for node in lst:
                row.append(node)
            board_copy.append(row)

        for i in range(len(board_copy)):
            board_copy[i].append(None)
            board_copy[i].append(None)
            board_copy[i].insert(0, None)
            board_copy[i].insert(0, None)
        board_copy.append([None] * (len(self.board[-1]) + 4))
        board_copy.append([None] * (len(self.board[-1]) + 4))
        board_copy.insert(0, [None, None, None, None])
        board_copy.insert(0, [None, None, None, None])

        # can be simplified later. Sets the the neighbours of the board's nodes.
        first_half = len(self.board) // 2 if shape == "d" else len(self.board)
        for i in range(first_half):
            for j in range(len(self.board[i])):
                self.board[i][j].neighbours["W"] = board_copy[i + 2][j + 2 - 1]
                self.board[i][j].neighbours["E"] = board_copy[i + 2][j + 2 + 1]
                self.board[i][j].neighbours["NW"] = board_copy[i + 2 - 1][j + 2 - 1]
                self.board[i][j].neighbours["NE"] = board_copy[i + 2 - 1][j + 2]
                self.board[i][j].neighbours["SW"] = board_copy[i + 2 + 1][j + 2]
                self.board[i][j].neighbours["SE"] = board_copy[i + 2 + 1][j + 2 + 1]
        if shape == "d":
            for i in range(first_half, first_half + 1):  # middle layer
                for j in range(len(self.board[i])):
                    self.board[i][j].neighbours["W"] = board_copy[i + 2][j + 2 - 1]
                    self.board[i][j].neighbours["E"] = board_copy[i + 2][j + 2 + 1]
                    self.board[i][j].neighbours["NW"] = board_copy[i + 2 - 1][j + 2 - 1]
                    self.board[i][j].neighbours["NE"] = board_copy[i + 2 - 1][j + 2]
                    self.board[i][j].neighbours["SW"] = board_copy[i + 2 + 1][j + 2 - 1]
                    self.board[i][j].neighbours["SE"] = board_copy[i + 2 + 1][j + 2]

            for i in range(first_half + 1, len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j].neighbours["W"] = board_copy[i + 2][j + 2 - 1]
                    self.board[i][j].neighbours["E"] = board_copy[i + 2][j + 2 + 1]
                    self.board[i][j].neighbours["NW"] = board_copy[i + 2 - 1][j + 2]
                    self.board[i][j].neighbours["NE"] = board_copy[i + 2 - 1][j + 2 + 1]
                    self.board[i][j].neighbours["SW"] = board_copy[i + 2 + 1][j + 2 - 1]
                    self.board[i][j].neighbours["SE"] = board_copy[i + 2 + 1][j + 2]

        # Set double neighbours
        """for i in range(len(self.board)):
            for j in range(len(self.board[i])): 
                node = self.board[i][j]
                for key in node.get_neighbours().keys():
                    if node.neighbours[key] != None:
                        node.get_double_neighbours()[key] = node.neighbours[key].neighbours[key]"""
        for lst in self.board:
            for node in lst:
                for key in node.neighbours.keys():
                    if node.neighbours[key] is not None:
                        node.double_neighbours[key] = node.neighbours[key].neighbours[key]
        # initialise the nodes without pegs.
        for touple in dead_pos_touples:
            x, y = touple
            self.board[touple[0]][touple[1]].kill()

    def get_nodes(self):  ## returns an array with the nodes in the board.
        nodes = []
        for row in self.board:
            for column in range(len(row)):
                nodes.append(row[column])
        return nodes

    def find_dead_nodes(self):  # helper function for finding nodes without pegs. Returns the id of the nodes as a list
       # nodes = self.get_nodes()
        dead_nodes = []

        for row in self.board:
            for node in row:
                if node.is_alive() == 0:
                    dead_nodes.append(node)

       # for i in range(len(nodes)):
        #    if nodes[i].is_alive() == 0:
         #       dead_nodes.append(nodes[i])
        return dead_nodes

    def find_alive_nodes(
            self):  # hepler function for finding nodes with pegs. Returns a list with the nodes that are alive.
        dead_nodes = self.find_dead_nodes()
        alive_nodes = []
        nodes = self.get_nodes()
        for node in nodes:
            if node not in dead_nodes:  # should maybe be checked by id?
                alive_nodes.append(node)
        return alive_nodes

    def get_available_moves(self):  # Returns moves should on form (Node, move_direction)
        ## We must concentrate on the dead nodes. Double neighbours can jump over neighbours,
        ## if the neighbour is alive.

        moves = []  # moves on form {node_id : direction (from dead_node)}
        dead_nodes = self.find_dead_nodes()
        for node in dead_nodes:
            neighbours = node.get_neighbours()
            double_neighbours = node.get_double_neighbours()
            for neighbour in neighbours.items():
                if neighbour[1] is None:
                    continue
                if neighbour[0] in double_neighbours and neighbour[1].is_alive() and double_neighbours[
                    neighbour[0]] is not None and double_neighbours[neighbour[0]].is_alive():
                    id = double_neighbours[neighbour[0]].get_id()  ##id
                    opposite_dir = neighbour[0]
                    direction = self.opposite_directions[opposite_dir]  ##direction
                    moves.append((id, direction))
        return moves

    def exists_available_moves(self): #function for speeding up the computations.

        moves = []  # moves on form {node_id : direction (from dead_node)}
        dead_nodes = self.find_dead_nodes()
        for node in dead_nodes:
            neighbours = node.get_neighbours()
            double_neighbours = node.get_double_neighbours()
            for neighbour in neighbours.items():
                if neighbour[1] is None:
                    continue
                if neighbour[0] in double_neighbours and neighbour[1].is_alive() and double_neighbours[
                    neighbour[0]] is not None and double_neighbours[neighbour[0]].is_alive():
                    return True
        return False


    def check_game_score(self): #returns if board is still playing, won, lost
        if self.node_count==1:
            return 100
        if self.exists_available_moves():
            return 0 #game is not over
        else:
            return -100 #game is lost

    def move(self, move):  # input: move on form (id, direction). Returns a board object iwth the applied move.
        nodes = self.get_nodes()
        id, dir = move
        node_to_move = nodes[id - 1]  # accounting for the discrepancy in node_id and 0-indexing of the list.
        neighbours = node_to_move.get_neighbours()
        neighbour = neighbours[dir]
        double_neighbours = node_to_move.get_double_neighbours()
        double_neighbour = double_neighbours[dir]
        node_to_move.kill()  # the node and neighbour is loses their pegs.
        neighbour.kill()
        double_neighbour.resurrect()
        self.node_count -= 1
        return self

    def get_board(self):  # returns the board as a nested list.
        return self.board

    def get_shape(self):  # returns the board's shape.
        return self.shape

    def get_size(self):  # returns the board's size.
        return self.size

    def state(self):  # returns the board as binary sting (1 = alive, 0 = dead).
        string = ""
        for line in self.board:
            for node in line:
                string += str(node.alive)
        return  string











