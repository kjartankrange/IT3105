import action_net
from game import *
import random
class Turnament:

    def __init__(self, net1, net2,rounds, round_interval, board_size):
        self.net1 = net1
        self.net2 = net2
        self.rounds = rounds
        self.round_interval = round_interval
        self.board_size = board_size
        self.results_table = {}
    
    def get_net_in_move(player_to_move):
        return net2 if player_to_move % 2 else net1

    def run(self):
        results = [] #encode  information as a list of 1s and 2s

        for round_ in range(self.round_interval,self.rounds+self.round_interval,self.round_interval):
            print(round_)
            games = [Game(board_size, random.choice([1,2]) ) for x in range(self.round_interval) ] #Todo board takes in player
            
            for game in games: 
                move = (2,2) #bogus move, this should be fixed generally, but crude solution works
                player_to_move = game.get_player()
                while not game.is_game_over(move):
                    #move = get_net_in_move(player_to_move).default_policy(game.get_state())
                    move = random.choice(game.get_valid_actions())
                    game.move(move)
                    player_to_move += 1
                
                winner = 2 if (player_to_move - 1) % 2 else 1 #last round
                results.append(winner)
            
            #register winners at each round
            self.results_table[round_] = (results.count(1),results.count(2))
    
            
    def show(self,graph=False):
        print("        Winners of turnament")
        print("{:>9} {:>9} {:>9}\n".format("round", "net1", "net2"))
        
        for key in self.results_table:
            print("{:>9} {:>9} {:>9}".format(key,self.results_table[key][0], self.results_table[key][1]) ) 

if __name__ == "__main__":
    net1 = "test"
    net2 = "test"
    rounds = 100
    round_interval = 10
    board_size = 4*4

    turnament = Turnament(net1, net2,rounds, round_interval, board_size)
    turnament.run()
    turnament.show()

