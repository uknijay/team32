from abc import ABC, abstractmethod
from Player import Player

class Strategy(Player, ABC):
    count = 0
    
    def __init__(self, name, money):
        super().__init__(name, money)
        
    @abstractmethod
    def addCount(value):
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
        
    def calcBet():
        return
    
    def decide_move():
        pass