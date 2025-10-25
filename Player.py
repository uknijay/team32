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
        self.map = {
            # --- Lowest possible total ---
            4:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},

            # --- Non-Ace hands (regular hard totals) ---
            5:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            6:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            7:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            8:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            9:  {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            10: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'H','A':'H',11:'H'},
            11: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'D','A':'D',11:'D'},
            12: {2:'H',3:'H',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            13: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            14: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            15: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            16: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},
            17: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S',11:'S'},

            # --- Ace-based hands (Ace fixed as 11) ---
            13: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},  # A,2
            14: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},  # A,3
            15: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},  # A,4
            16: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},  # A,5
            17: {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H','A':'H',11:'H'},  # A,6
            18: {2:'S',3:'D',4:'D',5:'D',6:'D',7:'S',8:'S',9:'H',10:'H','A':'H',11:'H'},  # A,7
            19: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S',11:'S'},  # A,8
            20: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S',11:'S'},  # A,9
            21: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S','A':'S',11:'S'},  # A,10
        }
    
    def hit(self):
        print(f"{self.name}: Hit!")
        self.get_card(1)
        v = self.hand_value()
        if v == 0:
            print(f"{self.name} went bust")
        elif v<21:
            self.decide_move()
    
    def stand(self):
        print(f"{self.name}: Stand!")
    
    def double(self):
        if len(self.hand) <= 2:
            print(f"{self.name}: Double!")
            self.bet *= 2
            print(f"{self.name}: Doubled their bet to {self.bet}")
        self.hit()
    
    def leave(self):
        print(f"{self.name} left the table")
        self.game.players.remove(self)
    def print_card(self,card):
        print(f"{card[0]} of {card[1]}")
            
    def hand_value(self):
        total = 0
        aces = 0

        for card in self.hand:
            val = self.game.value(card)
            total += val
            if card[0] == "Ace":
                aces += 1

        # Reduce total by 10 for as many Aces as needed to stay <=21
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
            for player in self.game.players:
                player.addCount(self.game.value(card))
            drawn.append(card)
            print(f"{self.name} drew a ",end="")
            self.print_card(card)
        self.hand.extend(drawn)
    
    @abstractmethod
    def stake(self):
        pass
    
    @abstractmethod
    def decide_move(self):
        pass
