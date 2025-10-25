from abc import ABC, abstractmethod

class Player(ABC):
    hand = []
    money = 0
    bet = 0
    name = None
    
    def __init__(self,name,money):
        self.name = name
        self.money = money
    
    def fold():
        pass
    
    def hit():
        pass
    
    def stand():
        pass
    
    def split():
        pass
    
    def double():
        pass
    
    def bet():
        pass
    
    def leave():
        pass