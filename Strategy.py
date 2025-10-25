from abc import ABC, abstractmethod
from Player import Player

class Strategy(Player, ABC):
    
    def __init__(self, name, money):
        self.count = 0
        super().__init__(name, money)
        
    @abstractmethod
    def addCount(self,value):
        pass
        
    @abstractmethod
    def calcBet():
        pass
    
    @abstractmethod
    def decide_move():
        pass
    
class HiLo(Strategy):
    def __init__(self, name, money):
        super().__init__(name, money)
           
    def decide_move():
        pass
    
    def addCount(self,value):
        pass
    
    def stake():
        pass