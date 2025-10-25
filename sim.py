import random
from itertools import product
values = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
suits = ["Hearts","Diamonds","Spades","Clubs"]
cards = list(product(values,suits))
random.shuffle(cards)

game_state = []

def get_card(n):
    hand = []
    for i in range(n):
        hand.append(cards.pop())
    return hand
    
def print_hand(hand):
    for value,suit in hand:
        print(f"{value} of {suit}")
        
def turn():
    return