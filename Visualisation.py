import networkx as nx
import matplotlib.pyplot as plt
import numpy as np




class Visualisation:

    G = nx.Graph()
    spacing = 10 ## should be available to update

    def __init__(self, shape, size): ## add functionality for shapes later
        self.shape = shape
        self.size = size

    #def update_board(self):

    def create_board(self, shape, size): ## function that creates nodes and edges.

        nodes, self.pos = self.create_nodes("triangle", size) ## the graph needs a position parameter to display the board correctly
        self.G.add_nodes_from(nodes) ## adding nodes
        edges = self.create_edges(self.pos, "triangle", self.spacing)
        self.G.add_edges_from(edges) ## adding edges

    def create_nodes(self, shape, size):
        pos = nx.spring_layout(self.G) ##creating a set position for every node.
        ##(remember testcase)
        node_number = 1 ## creating a unique node-id
        nodes = []
        #setting the positions, include separate parts for triangle and diamond later on
        for i in range(1, size + 1):
            for j in range(size - i + 1):
                pos[node_number] = [(5 * i) + 10 * j, 10 * i]
                nodes.append(node_number)
                node_number += 1
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
        return np.linalg.norm(distance_vector)





## Just testing the visualisation of the code


nummer1 = Visualisation( "rectangle",4)
nummer1.create_board( "rectangle",4)



nx.draw(
    nummer1.G,
    nummer1.pos,
    node_size=700,
    node_color = "red",
    #labels={node:node for node in nummer1.G.nodes()}
)

plt.show()








