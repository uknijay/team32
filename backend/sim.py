import random
from itertools import product
from Dealer import Dealer
from hilo import HiLo
from wong_halves import WongHalves
from Hi_opt_II import Hi_Opt_II
import matplotlib.pyplot as plt
import numpy as np

class Game:
    def __init__(self, player_data,deckCount,minStake,bankroll):
        
        self.playing = True
        self.rank = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]

        self.deckCount = deckCount
        self.minStake = minStake
        self.cards = self.shuffle()

        self.players = [fn(name, bankroll, self) for fn,name, in player_data]
        self.starting_players = self.players.copy()
        self.dealer = Dealer("Dealer", 0, self)
        self.game_state = []
        
    def shuffle(self):
        c = [list(card) for _ in range(self.deckCount) for card in product(self.rank, self.suits)]
        random.shuffle(c)
        return c
        
    def value(self, card):
        rank = card[0]
        if isinstance(rank, int):
            return rank
        elif rank == "Ace":
            return 11
        else:
            return 10
            
    def end_turn(self):
        dealer_val = self.dealer.hand_value()
        losers = []
        for player in self.players:
            player_val = player.hand_value()
            
            if player_val < dealer_val or player.bust:
                
                if player.money < self.minStake:
                    losers.append(player)
                    if len(self.players)==0:
                        self.playing = False
                        
            elif player_val > dealer_val:
                
                if player_val == 21 and len(player.hand) == 2:
                    player.money += player.bet*2.5
                else:
                    player.money += player.bet*2
                player.wins +=1
                
            else:
                player.money += player.bet
                
        for player in self.players:
            player.games += 1
        
        for player in losers:
            self.players.remove(player)
            
    
    def new_turn(self):
        if len(self.cards) < self.deckCount*52*0.25:
            for player in self.players:
                player.count = 0
                player.total_ace = 6*4
            self.cards = self.shuffle()
                 
        self.dealer.hand = []
        self.dealer.bust = False
        for player in self.players:
            player.bust = False
            player.bet = 0
            player.hand = []
            player.stake()
            player.money -= player.bet
        
            
        for player in self.players:
            player.get_card(2)
            
        self.dealer.get_card(1)
        
        for player in self.players:
            player.decide_move()
        
        if not all(player.bust == True for player in self.players):
            self.dealer.get_card(1)
            self.dealer.decide_move()
        
        self.end_turn()
            


def new_sim(simulations,rounds,starting_money, minimum_bet, player_list):
    shoe_shize = 6
    
    mean_data = [[0 for _ in range(rounds)] for _ in range(len(player_list))]
    all_data = [[] for _ in range(len(player_list))]
    

    for i in mean_data:
        i[0] = starting_money
    
    for j in range(simulations):
        game = Game(player_list,shoe_shize,minimum_bet,starting_money)
        sim_data = [[] for _ in range(len(player_list))]
        
        for i in range(1,rounds):
            if game.playing:
                game.new_turn()
            for n,player in enumerate(game.starting_players):
                mean_data[n][i]+=(player.money)/simulations
                sim_data[n].append(player.money)
                
        for n in range(len(player_list)):
            all_data[n].append(sim_data[n])
        
        
    turns = np.arange(rounds-1)
    for n in range(len(player_list)):
        arr = np.array(all_data[n])
        median = np.median(arr, axis=0)
        p25 = np.percentile(arr, 25, axis=0)
        p75 = np.percentile(arr, 75, axis=0)
        
        plt.plot(turns, median, label=player_list[n][0].__name__)
        plt.fill_between(turns, p25, p75, alpha=0.2)
        
    turns = [i for i in range(len(mean_data[0]))]
    for i in range(len(mean_data)):
        plt.plot(turns,mean_data[i],label = player_list[i][0].__name__)
        
    plt.legend()
    plt.show()

new_sim(100,10000,5000,10,[
        (WongHalves,"Dave"),
        (Hi_Opt_II,"John"),
        (HiLo,"Derek")
    ])  
    