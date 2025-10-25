from Strategy import Strategy


class WongHalves(Strategy):


    def __init__(self,name,money,game):
        super().__init__(name,money,game)
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


    def stake(self):
        self.betRamp = {
            0: self.game.minStake,
            1: self.game.minStake * 2,
            2: self.game.minStake * 4,
            3: self.game.minStake * 8,
            4: self.game.minStake * 12,
        }

        true_count = (self.count / (len(self.game.cards) / 52)).__floor__()
        if true_count <= 0:
            self.bet = self.game.minStake
        elif true_count > 0:
            if true_count in self.betRamp:
                self.bet = self.betRamp[true_count]
            else:
                self.bet = self.game.minStake * 12

        self.money -= self.bet
        

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
    

            
        