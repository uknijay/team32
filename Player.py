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
        self.map = {
            # --- Lowest possible total ---
            4:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H'},

            # --- Non-Ace hands (regular hard totals) ---
            5:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H'},
            6:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H'},
            7:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H'},
            8:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H'},
            9:  {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},
            10: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'H','A':'H'},
            11: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'D','A':'D'},
            12: {2:'H',3:'H',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H'},
            13: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H'},
            14: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H'},
            15: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H'},
            16: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H'},
            17: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S'},

            # --- Ace-based hands (Ace fixed as 11) ---
            13: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},  # A,2
            14: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},  # A,3
            15: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},  # A,4
            16: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},  # A,5
            17: {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H'},  # A,6
            18: {2:'S',3:'D',4:'D',5:'D',6:'D',7:'S',8:'S',9:'H',10:'H','A':'H'},  # A,7
            19: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S'},  # A,8
            20: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S'},  # A,9
            21: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S'},  # A,10
        }
    
    def hit(self):
        self.hand.extend(self.game.get_card(1))
        v = self.hand_value()
        if v<21 and v!=0:
            self.decide_move()
    
    def stand(self):
        pass
    
    def double(self):
        self.bet *= 2
        self.hit()
    
    def leave(self):
        self.game.players.remove(self)
    def print_hand(self):
        print(f"{self.name}'s hand:")
        for value,suit in self.hand:
            print(f"{value} of {suit}")
            
    def hand_value(self):
        v = 0
        for card in self.hand:
            v += self.game.value(card)
        if v<=21:
            return v
        else:
            for card in self.hand:
                if card[0] == "Ace":
                    card[0] = 1
                    return v - 10
            return 0
    
    @abstractmethod
    def stake():
        pass
    
    @abstractmethod
    def decide_move():
        pass