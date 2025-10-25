from abc import ABC, abstractmethod
from Player import Player

class Strategy(Player, ABC):
    count = 0
    
    def __init__(self, name, money):
        super().__init__(name, money)
        
    def calcBelt():
        pass
    
    def decide_move():
        pass