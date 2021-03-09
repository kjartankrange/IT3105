import networkx as nx
import matplotlib.pyplot as plt


class Game:  #Class for handling game logic and visualisation of a gamestate.

    graph = nx.Graph() ## a Game object has the following params: a graph, size, board, neighbour_dict, mapping to id, position for
                       # graph handling, and goal noades, which are the nodes in the outer edges for each player


    def __init__(self, size): #Inititialise the game object. Assumes games with diamond shaped boards.
        self.size = size
        self.position_to_node_id = {}
        self.board = self.create_board(size)
        self.neighbours = self.create_neighbours(size)
        self.goal_nodes = self.create_goal_nodes()



    def create_board(self, size): ## a board cell is represented by either 0 (empty), 1(player 1) or 2 (player 2).
        board = []
        self.pos = nx.spring_layout(self.graph)  ##creating a set position for every node.
        node_counter = 1
        for i in range(size):
            row = []
            for j in range(size):
                row.append(0) ##set empty, and initialise a mapping to the graph object
                self.graph.add_node(node_counter)
                self.position_to_node_id[(i,j)] = node_counter
                self.pos[node_counter] = [ -5*(i) + 5*j , -(i)*5 - 5*j ]
                node_counter += 1
            board.append(row)
        return board ## returns a n x n dimensional board, which is a 45 degree rotation of the hexagonal board (n is the size)


    def get_game(self):
        return self

    def get_node_id(self, position):
        return self.position_to_node_id[position]

    def create_neighbours(self, size):
        neighbours = {}
        for i in range(size):
            for j in range(size):
                node_neighbours = []
                if i - 1 >= 0:
                    node_neighbours.append((i-1,j))
                    if j + 1 < size:
                        node_neighbours.append((i-1, j+1))
                if j - 1 >= 0:
                    node_neighbours.append((i, j-1))
                if j + 1 < size:
                    node_neighbours.append((i, j+1))
                if i + 1 < size:
                    node_neighbours.append((i+1, j))
                    if j -1 >= 0:
                        node_neighbours.append((i+1, j-1))
                neighbours[(i,j)] = node_neighbours
                node_id = self.get_node_id((i,j)) #find the node_id
                for neighbour in node_neighbours:
                    x_pos , y_pos = neighbour
                    neighbour_id = self.get_node_id((x_pos, y_pos))
                    self.graph.add_edge(node_id, neighbour_id) #Create edge in the networkx object
        return neighbours

    def get_neighbours(self, position):
        return self.neighbours[position]

    def occupied_by(self, position): #returns 0 if empty, 1 if occupied by player 1, 2 by player 2
        x_pos ,y_pos = position
        return self.board[x_pos][y_pos]

        # must find end nodes in both outer edges
    def create_goal_nodes(self):


        player_one_start = self.board[0]
        player_one_end = self.board[len(self.board) -1]
        player_two_start = self.board[:][0]
        player_two_end = self.board[:][len(self.board) - 1]
        return [player_one_start, player_one_end], [player_two_start,player_two_end]


    def is_game_over(self, move): #a move should be on the form (player_id, (x_pos, y_pos))
            player_id = move[0]
            position = move[1]

            neighbours = self.get_neighbours(position)

            values =[]
            for neighbour in neighbours: ##check for no neighbours of same colour to speed up process
                value = self.board[neighbour[0]][neighbour[1]]
                values.append(value)
            if player_id == 1:
                if 1 not in values:
                    return False
            if player_id == 2:
                if 2 not in values:
                    return False

            stack = [position]
            visited = []
            start_nodes, goal_nodes = self.goal_nodes[player_id - 1]
            filled_cells = []
            filled_cells.append(position)

            while len(stack) > 0 :

                node = stack.pop()
                visited.append(node)

                for neighbour in neighbours:

                    x_pos, y_pos = neighbour
                    node = self.board[x_pos][y_pos]
                    if node == player_id and neighbour not in visited:
                        filled_cells.append(neighbour)
                        stack.append(neighbour)
                        visited.append(neighbour)
                        neighbours = self.get_neighbours((x_pos,y_pos))


            if sum(start_nodes) > 0 and sum(goal_nodes) >0:
                start, end = False, False
                for node in filled_cells:
                    i, j = node

                    if player_id == 1:
                        if i == 0:
                            start = True
                        if i == len(self.board) - 1:
                            end = True
                    if player_id == 2:
                        if j== 0:
                            start = True
                        if j == len(self.board) -1 :
                            end = True
                return start and end


            return False








    def move(self, move, player): #places a player
        if self.can_move(move):
            x_pos = move[0]
            y_pos = move[1]
            self.board[x_pos][y_pos] = player
        else:
            raise Exception("Invalid move")

    def can_move(self, move): # checks if a hex player can make the desired move (move on form (i, j))
        x_pos = move[0]
        y_pos = move[1]
        return not self.board[x_pos][y_pos]

    def visualise(self):
        vis = nx.draw(self.graph, self.pos, node_color ="lightgrey",
                       node_size=700)
        plt.show()

#data structure: array of player . are connected if same player

# find : check if p and q have same player
# connect if
# path compression


g = Game(4)
print(g.is_game_over(((1), (1,1))))
g.visualise()

g.move((0,0),1)
g.move((1,0),1)
g.move((1,1),1)
g.move((0,1),1)
#g.move((2,2),1)
#g.move((1,2),1)
#g.move((2,1),2)
#g.move((3,1),1)
print("The game is over", g.is_game_over(((1), (3,1))))
#g.move((1,1),1)

#print(g.is_game_over((1,(2,1))))





