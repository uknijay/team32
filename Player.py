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
    
    def value(card):
        # card = (value,suit) e.g (King, Heart)
        if isinstance(card[0], int):
            return card[0]
        
        elif card == "Ace":
            return 11
        
        else:
            return 10