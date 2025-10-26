from Strategy import Strategy

class HiLo(Strategy):


    def __init__(self, name, money, game):
        super().__init__(name, money, game)

        self.tags = {
            2:  +1,
            3:  +1,
            4:  +1,
            5:  +1,
            6:  +1,
            7:   0,
            8:   0,
            9:   0,
            10: -1,
            11: -1,  
        }
        self.count = 0


    def addCount(self, value):

        if value in self.tags:
            self.count += self.tags[value]


    def stake(self):

        self.betRamp = {
            0: self.game.minStake,        
            1: self.game.minStake * 2,
            2: self.game.minStake * 3,
            3: self.game.minStake * 4,
            4: self.game.minStake * 5,
            5: self.game.minStake * 6,
        }


        decks_remaining = max(1, len(self.game.cards) / 52)
        true_count = self.count / decks_remaining


        if true_count <= 0:
            bet = self.game.minStake
        else:
            bet = self.betRamp.get(int(true_count), self.game.minStake * 8)


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