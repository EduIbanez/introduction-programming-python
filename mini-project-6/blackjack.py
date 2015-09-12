# Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-6/images/cards.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-6/images/cards_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.list_cards = []

    def __str__(self):
        cards = ""
        for index in range(len(self.list_cards)):
            if index < len(self.list_cards) - 1:
                cards += str(self.list_cards[index]) + ", "
            else:
                cards += str(self.list_cards[index])
        return "Hand contains " + cards

    def add_card(self, card):
        self.list_cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_ace = False
        for card in self.list_cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                has_ace = True
        if not has_ace:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        for index in range(len(self.list_cards)):
            self.list_cards[index].draw(canvas, [pos[0] + (CARD_SIZE[0] + 30) * index, pos[1]])

# define deck class
class Deck:
    def __init__(self):
        self.list_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.list_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.list_cards)

    def deal_card(self):
        card = None
        if len(self.list_cards) > 0:
            card = self.list_cards.pop(0)
        else:
            print("Empty deck")
        return card
    
    def __str__(self):
        cards = ""
        for index in range(len(self.list_cards)):
            if index < len(self.list_cards) - 1:
                cards += str(self.list_cards[index]) + ", "
            else:
                cards += str(self.list_cards[index])
        return "Deck contains " + cards

#define event handlers for buttons
def deal():
    global outcome, message, score, in_play, deck, player, dealer
    if in_play:
        message = "You lose"
        score -= 1
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
        player = Hand()
        dealer = Hand()
        for index in range(2):
            player.add_card(deck.deal_card())
            dealer.add_card(deck.deal_card())
        in_play = True
        outcome = "Hit or stand?"
        message = ""

def hit():
    global outcome, message, score, in_play
    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
        # if busted, assign messages
        if player.get_value() > 21:
            outcome = "New deal?"
            message = "You went bust. You lose"
            in_play = False
            score -= 1

def stand():
    global outcome, message, score, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            message = "Dealer went bust. You win"
            score += 1
        else:
            if player.get_value() <= dealer.get_value():
                message = "You lose"
                score -= 1
            else:
                message = "You win"
                score += 1
        in_play = False
        outcome = "New deal?"

# draw handler
def draw(canvas):
    canvas.draw_text("Blackjack", (100, 100), 40, "Gold")
    canvas.draw_text("Score: " + str(score), (420, 100), 30, "Black")
    canvas.draw_text("Dealer", (60, 175), 25, "Black")
    canvas.draw_text(message, (220, 175), 25, "Black")
    dealer.draw(canvas, (60, 200))
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          (CARD_BACK_CENTER[0] + 60, CARD_BACK_CENTER[1] + 200), CARD_BACK_SIZE)
    canvas.draw_text("Player", (60, 375), 25, "Black")
    canvas.draw_text(outcome, (220, 375), 25, "Black")
    player.draw(canvas, (60, 400))

# initialization frame
frame = simplegui.create_frame("Blackjack", 702, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 50)
frame.add_button("Hit",  hit, 50)
frame.add_button("Stand", stand, 50)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
