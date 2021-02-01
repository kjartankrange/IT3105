import networkx as nx
import matplotlib.pyplot as plt



class Visualisation:

    G = nx.Graph()
    spacing = 10 ## should be available to update

    def __init__(self, shape, size):
        self.shape = shape
        self.size = size

    #def update_board(self):


    def create_board(self, shape, size):

        ##number_of_nodes = sum(range(size +1))
        self.pos = nx.spring_layout(self.G, scale=2, seed=84)
        ##helper function for creating boards. (remember testcase)
        counter = 1
        for i in range(1, size +1 ):
            for j in range(size  - i + 1):
                self.pos[counter] = [(5* i ) + 10*j, 10*i]
                self.G.add_node(counter)
                counter += 1
        self.G.add_edge(4,7)






nummer1 = Visualisation( "rectangle",4)
nummer1.create_board( "rectangle",4)

print(nummer1.G.edges)

nx.draw(
    nummer1.G,
    nummer1.pos,
    node_size=500,
    alpha=0.9,
    labels={node:node for node in nummer1.G.nodes()}
)

print(nummer1.G , "hello")
nx.draw_networkx_edge_labels(nummer1.G, nummer1.pos)
plt.show()








