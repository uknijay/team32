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

    def addCount(self, value):
        self.count += self.tags[value]


    def stake(self):
        self.betRamp = {
            0: self.game.minStake,         # 15
            1: self.game.minStake * 2,     # 30
            2: self.game.minStake * 3,     # 45
            3: self.game.minStake * 4,     # 60
            4: self.game.minStake * 5,     # 75
            5: self.game.minStake * 6,     # 90, optional max cap
        }

        true_count = self.count / (len(self.game.cards) / 52)

        if true_count <= 0:
            bet = self.game.minStake
        else:
            bet = self.betRamp.get(int(true_count), self.game.minStake * 12)

        # ensure bet is at least minStake, and at most 20% of bankroll
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
    

            
        