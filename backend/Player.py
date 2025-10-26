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
        self.bust = False
        self.wins = 0
        self.games = 0
        self.cap = 1
        self.set_map()
    
    def hit(self):
        self.get_card(1)
        v = self.hand_value()
        if v == 0:
            pass
        elif v<21:
            self.decide_move()
    
    def double(self):
        if len(self.hand) <= 2 and self.money>self.bet:
            self.money -= self.bet
            self.bet *= 2
            self.get_card(1)
        else:
            self.hit()
    
    def leave(self):
        self.game.players.remove(self)
        
    def print_card(self,card):
        pass
            
    def hand_value(self):
        total = 0
        aces = 0

        for card in self.hand:
            val = self.game.value(card)
            total += val
            if card[0] == "Ace":
                aces += 1

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        if total > 21:
            self.bust = True
            return 0

        return total

    
    def get_card(self, n):
        drawn = []
        for _ in range(n):
            card = self.game.cards.pop()
            self.addCount(self.game.value(card))
            drawn.append(card)
        self.hand.extend(drawn)
        
    def set_map(self):
        self.map = {
                    4: {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    5: {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    6: {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    7: {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    8: {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    9: {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    10: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'H',11:'H'},
                    11: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'D',11:'H'},
                    12: {2:'H',3:'H',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    13: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    14: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    15: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    16: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
                    17: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
                    18: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
                    19: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
                    20: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
                    21: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
                } 
    
    @abstractmethod
    def stake(self):
        pass
    
    @abstractmethod
    def decide_move(self):
        pass
