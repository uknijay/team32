from Player import Player
from Strategy import Strategy

class Dealer(Strategy):
    def __init__(self, name, money,game):
        super().__init__(name, money, game)
        
    def calcBet():
        pass
    
    def stake():
        pass
    
    def addCount(value):
        return
    
    def decide_move(self):
        v = 0
        for card in self.hand:
            v+=self.game.value(card)
        if v<17:
            self.hit()