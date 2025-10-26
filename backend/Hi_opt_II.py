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
        self.true_count_play = (self.count / (len(self.game.cards) / 52))
        self.true_count_bet = int((self.count + self.total_ace) / (len(self.game.cards) / 52))

    def stake(self):
        self.calc_true_count()
        # print(self.true_count_bet)
        if self.true_count_bet <= 0:
            bet = 1           # 1 × minStake
        elif self.true_count_bet == 1:
            bet = 2
        elif self.true_count_bet == 2:
            bet = 3
        elif self.true_count_bet == 3:
            bet = 4
        elif self.true_count_bet == 4:
            bet = 5
        else:  # TC >= 5
            bet = 6

        
        bet*=self.game.minStake
        bet = max(self.game.minStake, min(bet, self.money // self.cap))
        self.bet = bet

    def decide_move(self):
        total = self.hand_value()
        dealer = self.game.value(self.game.dealer.hand[0])
        self.set_map()
        
        if self.true_count_play >= 2:
            self.map[9][3] = 'D'
            self.map[11][11] = 'D'
            self.map[12][3] = 'S'
            self.map[16][10] = 'S'
        elif self.true_count_play >= 1:

            self.map[12][13] = 'H'
        elif self.true_count_play >= 0:
            self.map[9][2] = 'H'
            self.map[11][11] = 'H'
        elif self.true_count_play >= -1:
            self.map[16][10] = 'H'
        elif self.true_count_play >= -2:
            self.map[12][5] = 'H'
            self.map[13][2] = 'H'
        else:
            self.map[13][3] = 'H'
        
        action = self.map[total][dealer]
        if action == 'H':
            self.hit()
        elif action == 'S':
            pass
        elif action == 'D':
            self.double()
