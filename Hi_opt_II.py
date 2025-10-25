import math

from Strategy import Strategy

class Hi_Opt_II(Strategy):

    def __init__(self, name, money, game):
        super().__init__(name, money, game)
        self.count = 0
        self.true_count_play = 0
        self.true_count_bet = 0
        self.ace_count = 0
        self.total_ace = len(self.game.cards) / 13
        self.total_cards = len(self.game.cards)

    def addCount(self, value):
        if value in [2,3,6,7]:
            self.count += 1
        elif value in [4,5]:
            self.count += 2
        elif value in [8,9]:
            self.count += 0
        elif value == 10:
            self.count -= 2
        elif value == 11:
            self.ace_count += 1

    def calc_true_count(self):
        self.true_count_bet = (self.count + ((self.total_ace * ((self.total_cards - len(self.game.cards)) / self.total_cards))- self.ace_count))

    def stake(self):
        self.calc_true_count()
        if self.true_count_bet <= 0:
            bet = 1           # 1 × minStake
        elif self.true_count_bet == 1:
            bet = 1
        elif self.true_count_bet == 2:
            bet = 2
        elif self.true_count_bet == 3:
            bet = 3
        elif self.true_count_bet == 4:
            bet = 4
        else:  # TC >= 5
            bet = 5

        
        bet*=self.game.minStake
        bet = max(self.game.minStake, min(bet, self.money // 5))
        self.bet = bet

    def decide_move(self):
        total = self.hand_value()
        dealer = self.game.value(self.game.dealer.hand[0])   
        action = self.map[total][dealer]
        if action == 'H':
            self.hit()
        elif action == 'S':
            self.stand()
        elif action == 'D':
            self.double()
