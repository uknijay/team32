import random
from itertools import product
from Dealer import Dealer
from Strategy import HiLo  
from wong_halves import WongHalves

class Game:
    def __init__(self, player_data,deckCount,minStake):
        
        self.rank = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        
        self.players = [WongHalves(name, money, self) for name, money in player_data]
        self.dealer = Dealer("Dealer", 0,self)
        self.game_state = []
        
        self.deckCount = deckCount
        self.minStake = minStake       
        
        self.cards = self.shuffle()  
        
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
            
    
    
    # def end_turn(self):
    #     for player in self.players:
    #         if player.game.hand_value() > self.dealer.
            
    
    def new_turn(self):
        if len(self.cards) < self.deckCount*52*0.25:
            for player in self.players:
                player.count = 0
                 
        for player in self.players:
            player.stake()
            
        for player in self.players:
            player.get_card(2)
            
        self.dealer.get_card(1)
        
        for player in self.players:
            player.decide_move()
            
        self.dealer.get_card(1)
        self.dealer.decide_move()


if __name__ == "__main__":
    game = Game([
        ("Dave", 500),
        ("John", 500)
    ],6,15)
    game.new_turn()
