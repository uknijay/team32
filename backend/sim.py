import random
from itertools import product
from Dealer import Dealer
from hilo import HiLo
from wong_halves import WongHalves
from Hi_opt_II import Hi_Opt_II

class Game:
    def __init__(self, player_data,deckCount,minStake):
        
        self.playing = True
        self.rank = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]

        self.deckCount = deckCount
        self.minStake = minStake
        self.cards = self.shuffle()

        self.players = [fn(name, money, self) for fn,name, money in player_data]
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
            
        if len(self.players) == 0:
            self.playing = False
    
    def new_turn(self):
        if len(self.cards) < self.deckCount*52*0.25:
            for player in self.players:
                player.count = 0
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