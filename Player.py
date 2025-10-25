from abc import ABC, abstractmethod

class Player(ABC):
    
    
    def __init__(self,name,money,game):
        self.hand = []
        self.money = 0
        self.bet = 0
        self.name = None
        self.name = name
        self.money = money
        self.game = game
    
    def hit(self):
        self.hand.extend(self.game.get_card(1))
    
    def stand():
        pass
    
    def split():
        pass
    
    def double(self):
        bet *= 2
        self.hit()
    
    def leave(self):
        from sim import players
        players.remove(self)
    def print_hand(self):
        print(f"{self.name}'s hand:")
        for value,suit in self.hand:
            print(f"{value} of {suit}")
    
    @abstractmethod
    def stake():
        pass