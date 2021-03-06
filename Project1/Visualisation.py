
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np





class Visualisation:

    G = nx.Graph()
    spacing = 10 ## should be available to update
    color_map = []
    pos = []

    def __init__(self, board): ## initialise the visualisation object.
        self.shape = board.get_shape()
        self.size = board.get_size()
        self.create_board(self.shape, self.size)
        self.make_dead(board.get_board())

    def create_board(self, shape, size): ## function that creates nodes and edges.

        nodes, self.pos = self.create_nodes(shape, size) ## the graph needs a position parameter to display the board correctly
        self.G.add_nodes_from(nodes) ## adding nodes
        edges = self.create_edges(self.pos, shape, self.spacing)
        self.G.add_edges_from(edges) ## adding edges


    def create_nodes(self, shape, size):
        pos = nx.spring_layout(self.G) ##creating a set position for every node.
        ##(remember testcase)
        node_number = 1 ## creating a unique node-id
        nodes = []
        #setting the positions for the nodes. Different layout for triangle and diamond shape.
        if shape == ("t"):
            for i in range(1, size + 1):
                for j in range(size - i + 1):
                    pos[node_number] = [(5 * i) + 10 * j, 10 * i]
                    nodes.append(node_number)
                    node_number += 1
                    self.color_map.append("black")
        elif shape == "d":
            for i in range(1,  size + 1):
                for j in range(size - i + 1):
                    pos[node_number] = [(5 * i) + 10 * j, 10 * (i)]
                    nodes.append(node_number)
                    node_number += 1
                    self.color_map.append("black")
            for i in range(1,  size):
                for j in range(1,size - i + 1):
                    pos[node_number] = [(5*(i- 1)) + 10 * j, -10 * (i- 1) ] #need some comments here presumably
                    nodes.append(node_number)
                    node_number += 1
                    self.color_map.append("black")
        return nodes, pos


    def create_edges(self, pos, shape, distance): ## helper function for returning neighbours as list
       ## if shape == "triangle": to be added later
        proximity_cutoff = np.sqrt(distance **2 + (distance/2)**2) ## a node is within another's proximiy if it has distance <= sqrt(distance**2 + distance/2 **2)
        edge_list  = []

        ## finding neighbouring edges
        for i in range(1, len(pos)+1):
            for j in range(i +1, len(pos)+1):
                if self.dist(pos[i], pos[j]) <= proximity_cutoff: ## include if distance is less than the cutoff
                    edge_list.append((i,j))
        return edge_list

    def dist(self, u,v):   ## helper method for computing distances in space, using np.linalg.norm
        distance_vector = [u[0] - v[0], u[1]- v[1]]
        return np.linalg.norm(distance_vector) #finding norm of vector

    def make_dead(self, status): ## input is a board, which is a list populated with nodes
        status = self.format_board(status)
        for i in range(len(status)):
            if status[i].is_alive() == 0:
                self.color_map[i] = "Lightgrey" # dead nodes have a lightgrey colour.
            elif status[i].is_alive() == 1:
                self.color_map[i] = "Black"


    #format the state appropriateley.
    def format_board(self, status):
        formatted_list = []
        if self.shape == "t":
            for row in status:
                for node in range(len(row)-1, -1, -1):
                    formatted_list.insert(0,row[node])
        elif self.shape == "d":
            middle_index = len(status)//2
            for i in range(middle_index ,-1,-1):
                for j in range(len(status[i])):
                    formatted_list.append(status[i][j])
            for i in range(middle_index+1, len(status)):
                for j in range(len(status[i])):
                    formatted_list.append(status[i][j])

        return formatted_list


    def visualise(self): #returns a visiualisation to be plotted.

        return nx.draw(self.G, self.pos,
                node_size= 700,
                node_color = self.color_map
                )
