from Strategy import Strategy
from sim import cards
from sim import Game


class WongHalves(Strategy):


    def __init__(self,game:Game):
        super().__init__("Wong Halves",game)
        self.tags = {
            2:  +0.5,
            3:  +1.0,
            4:  +1.0,
            5:  +1.5,
            6:  +1.0,
            7:  +0.5,
            8:   0.0,
            9:  -0.5,
            10: -1.0,
            11: -1.0,
        }
        self.count = 0
        self.game = game
    


    def addCount(self, value):
        self.count += self.tags[value]


    def calcBet(self):
        self.betRamp = {
            0: self.game.minStake,
            1: self.game.minStake * 2,
            2: self.game.minStake * 4,
            3: self.game.minStake * 8,
            4: self.game.minStake * 12,
        }

        true_count = (self.count / (len(cards) / 52)).__floor__()
        if true_count <= 0:
            bet_amount = self.game.minStake
        elif true_count > 0:
            if true_count in self.betRamp:
                bet_amount = self.betRamp[true_count]
            else:
                bet_amount = self.game.minStake * 12
            
        self.place_bet(bet_amount)

    def decide_move(self):
        total = self.game.hand_value()
        dealer = self.game.dealer.hand[0][0]    
        action = self.strategy_map[(total, False, dealer)]
        print(action)
        if action == 'H':
            self.hit()
        elif action == 'S':
            self.stand()
        elif action == 'D':
            self.double()
    

            
        