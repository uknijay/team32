import random
from itertools import product
from Player import Player
from Strategy import *
values = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
suits = ["Hearts","Diamonds","Spades","Clubs"]
cards = list(product(values,suits))
random.shuffle(cards)

game_state = []

players = [HiLo("Dave",2000),HiLo("John",1500)]

def get_card(n):
    hand = []
    for i in range(n):
        c = cards.pop()
        game_state.append(c)
        hand.append(c)
    return hand
    
def print_hand(hand):
    for value,suit in hand:
        print(f"{value} of {suit}")
        
def newTurn():
    for player in players:
        player.hand = get_card(2)
    