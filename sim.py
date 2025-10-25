import random
from itertools import product
from Player import Player
from Dealer import Dealer
from Strategy import *
rank = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
suits = ["Hearts","Diamonds","Spades","Clubs"]
cards = list(product(rank,suits))
random.shuffle(cards)

game_state = []

players = [HiLo("Dave",2000),HiLo("John",1500)]
dealer = Dealer("Bob",0)

def value(card):
        if isinstance(card[0], int):
            return card[0]
        
        elif card == "Ace":
            return 11
        
        else:
            return 10

def get_card(n): 
    hand = []
    for i in range(n):
        c = cards.pop()
        for player in players:
            player.addCount(value(c))
        hand.append(c)
    return hand
    

        
def newTurn():
    for player in players:
        player.hand = get_card(2)
    dealer.hand = get_card(1)
    
    for player in players:
        player.print_hand()
    dealer.print_hand()
    
