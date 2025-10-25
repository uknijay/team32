import random
from itertools import product
from Dealer import Dealer
from Strategy import HiLo  


class Game:
    def __init__(self, player_data,deckcount,minStake):
        
        self.rank = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        
        self.players = [HiLo(name, balance) for name, balance in player_data]
        self.dealer = Dealer("Dealer", 0)
        self.game_state = []
        
        self.deckCount = deckcount
        self.minStake = minStake       
        
        self.cards = self.shuffle()  
        
    def shuffle(self):
        return random.shuffle(self.deckcount*list(product(self.rank, self.suits)))
        
    def value(self, card):
        rank = card[0]
        if isinstance(rank, int):
            return rank
        elif rank == "Ace":
            return 11
        else:
            return 10
        
    def hand_value(self):
        v = 0
        for card in self.hand:
            v += game.value(card)
        if v<=21:
            return v
        else:
            for card in self.hand:
                if card[0] == "Ace":
                    card[0] = 1
                    return v - 10
            return 0
            
    def get_card(self, n):
        drawn = []
        for _ in range(n):
            card = self.cards.pop()
            for player in self.players:
                player.addCount(self.value(card))
            drawn.append(card)
        return drawn
    
    def new_turn(self):
        if len(self.cards) < self.deckCount*52*0.25:
            for player in self.players:
                player.count = 0
                 
        for player in self.players:
            player.stake()
            
        for player in self.players:
            player.hand = self.get_card(2)
            
        self.dealer.hand = self.get_card(1)
        
        for player in self.players:
            player.decide_move()
            
        self.dealer.game.get_card(1)
        self.dealer.decide_move()


if __name__ == "__main__":
    game = Game([
        ("Dave", 500),
        ("John", 500)
    ],6,15)
    game.new_turn()
