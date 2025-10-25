import random
from itertools import product
from Dealer import Dealer
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
            
    
    
    def end_turn(self):
        for player in self.players:
            if player.hand_value() > self.dealer.hand_value():
                player.money += player.bet
                print(f"{player.name} won £{player.bet}")
            else:
                print(f"{player.name} lost £{player.bet}")
                player.money -= player.bet
                
        for player in self.players:
            print(f"{player.name}: {player.hand}")
        print(f"{self.dealer.name}: {self.dealer.hand}")
            
    
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
            print(f"{player.name} staked {player.bet}")
        
            
        for player in self.players:
            player.get_card(2)
            
        self.dealer.get_card(1)
        
        for player in self.players:
            player.decide_move()
        
        if not all(player.bust == True for player in self.players):
            self.dealer.get_card(1)
            self.dealer.decide_move()
        
        self.end_turn()
            
        


if __name__ == "__main__":
    game = Game([
        ("Dave", 500),
        ("John", 500)
    ],6,15)
    for i in range(100):
        game.new_turn()
        print(f"Game: {i}")
    
    for player in game.players:
        print(f"{player.name}: final moneys {player.money}")