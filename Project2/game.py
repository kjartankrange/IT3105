import networkx as nx
import matplotlib.pyplot as plt


class Game:  #Class for handling game logic and visualisation of a gamestate.

    graph = nx.Graph() ## a Game object has the following params: a graph, size, board, neighbour_dict, mapping to id, position for
                       # graph handling, and goal noades, which are the nodes in the outer edges for each player


    def __init__(self, size, player): #Inititialise the game object. Assumes games with diamond shaped boards.
        self.size = size
        self.player = player
        self.position_to_node_id = {}
        self.board = self.create_board(size)
        self.neighbours = self.create_neighbours(size)
        self.goal_nodes = self.create_goal_nodes()



    def create_board(self, size): ## a board cell is represented by either 0 (empty), 1(player 1) or 2 (player 2).
        board = []
        self.pos = nx.spring_layout(self.graph)  ##creating a set position for every node.
        node_counter = 1
        move_distribution = []
        for i in range(size):
            row = []
            for j in range(size):
                move_distribution.append((i,j))
                row.append(0) ##set empty, and initialise a mapping to the graph object
                self.graph.add_node(node_counter)
                self.position_to_node_id[(i,j)] = node_counter
                self.pos[node_counter] = [ -5*(i) + 5*j , -(i)*5 - 5*j ]
                node_counter += 1
            board.append(row)
        self.move_distribution = move_distribution
        return board ## returns a n x n dimensional board, which is a 45 degree rotation of the hexagonal board (n is the size)

    def get_board(self):
        return self
    
    def get_move_distribution(self):
        return self.move_distribution

    def get_node_id(self, position): ##position on form (x,y)
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

    def get_neighbours(self, position): #returns list of neighbours from position
        return self.neighbours[position]


        # must find end nodes in both outer edges
    def create_goal_nodes(self):

        player_one_start = self.board[0]
        player_one_end = self.board[len(self.board) -1]
        player_two_start = []
        player_two_end = []
        for row in self.board: ## This doesnt work. Doesnt update. Will fix later
            player_two_start.append(row[0])
            player_two_end.append(row[len(self.board) -1])

        return [player_one_start, player_one_end], [player_two_start,player_two_end]

    # Can use parameters player_id, move ?
    def is_game_over(self, position): #position should be on the form (x_pos, y_pos)
            #player_id = 2 if self.player == 1 else 1
            player_id = self.player
            neighbours = self.get_neighbours(position)
            values =[]

            for neighbour in neighbours: ##check for no neighbours of same colour to speed up process
                value = self.board[neighbour[0]][neighbour[1]]
                values.append(value)
            if player_id not in values:
                return False

            stack = [position]
            visited = []
            start_nodes, goal_nodes = self.goal_nodes[player_id - 1]
            filled_cells = []
            filled_cells.append(position)

            while len(stack) > 0 :
                node = stack.pop()
                visited.append(node)
                neighbours = self.get_neighbours(node)
                for neighbour in neighbours:

                    x_pos, y_pos = neighbour
                    colour = self.board[x_pos][y_pos]
                    if colour == player_id and neighbour not in visited:
                        filled_cells.append(neighbour)
                        stack.append(neighbour)
                        visited.append(neighbour)


            if player_id == 2:
                start_nodes = list(zip(*self.board))[0]
                goal_nodes = list(zip(*self.board))[self.size -1]
            if player_id in start_nodes  and player_id in goal_nodes :
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
                if start and end:
                    #print("Player ", player_id, " won!!!")
                    return self.player
                return start and end

            return False

    def sim_copy(self):
        return Game(self.size, self.player)

    def move(self, move): #places a player
        if self.can_move(move):
            x_pos = move[0]
            y_pos = move[1]
            #print("player ", self.player, "placed a piece on : ", move)
            self.board[x_pos][y_pos] = self.player
            if self.player == 1:
                self.player = 2
            elif self.player == 2:
                self.player = 1
        else:
            raise Exception("Invalid move")

    def get_player(self):
        return self.player

    def get_valid_actions(self):
        valid_actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    valid_actions.append((i, j))
        return valid_actions


    def can_move(self, move): # checks if a hex player can make the desired move (move on form (i, j))
        x_pos = move[0]
        y_pos = move[1]
        return not self.board[x_pos][y_pos]

    def get_state(self):
        result = ""
        for row in self.board:
            result += "".join(map(str,row))
        return result


    def visualise(self):
        colour_map = []
        for row in self.board:
            for node in row:
                if node == 1:
                    colour_map.append("#ff4d4d")
                elif node == 2:
                    colour_map.append("#4d4dff")
                else:
                    colour_map.append("lightgrey")

        vis = nx.draw(self.graph, self.pos, node_color =colour_map,
                       node_size=700)
        plt.show()

#data structure: array of player . are connected if same player

# find : check if p and q have same player
# connect if
# path compression

if __name__ == "__main__":
    import random
    g = Game(5, 1)

    move = random.choice(g.get_valid_actions())

    g.move( move)
    g.visualise()
    while not g.is_game_over( move):

        move = random.choice(g.get_valid_actions())
        g.move( move)
        g.visualise()

