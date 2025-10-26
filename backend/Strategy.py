from abc import ABC, abstractmethod
from Player import Player

class Strategy(Player, ABC):
    
    def __init__(self, name, money, game):
        self.count = 0
        super().__init__(name, money, game)
        
    @abstractmethod
    def addCount(self,value):
        pass
    
    @abstractmethod
    def decide_move(self):
        pass
