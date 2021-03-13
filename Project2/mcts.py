

class MCTS:
    def __init__(self, ann, sim_time, board):
        self.ann = ann
        self.time = sim_time
        self.board = board
    
    def uct_search(self):
        time_left = self.time
        while time_left>0:
            sim_board = self.board.copy() # does this work?
            self.simulate(sim_board)
            time_left-=1
        self.board.set_position(self)
        return self.select_move(self.board, s, c)

    def simulate(self, board):
        pass
    def select_move(self, board, s ,c):
        pass
