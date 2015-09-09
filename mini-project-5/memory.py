# Memory

import simpleguitk as simplegui
import random

WIDTH_CARD = 70
HEIGHT_CARD = 135

# helper function to initialize globals
def new_game():
    global deck_cards, exposed, state, turns
    deck_cards = list(range(8)) + list(range(8))
    random.shuffle(deck_cards)
    state = 0
    turns = 0
    exposed = []
    for number in range(0, 16):
        exposed.append(False)
    label.set_text("Turns = " + str(turns))

# define event handlers
def mouseclick(pos):
    global state, first_choice, second_choice, turns
    position = pos[0] // WIDTH_CARD
    if state == 0:
        exposed[position] = True
        first_choice = position
        state = 1
    elif state == 1:
        if exposed[position] == False:
            exposed[position] = True
            second_choice = position
            state = 2
            turns += 1
            label.set_text("Turns = " + str(turns))
    else:
        if exposed[position] == False:
            if deck_cards[first_choice] != deck_cards[second_choice]:
                exposed[first_choice] = False
                exposed[second_choice] = False
            exposed[position] = True
            first_choice = position
            state = 1

# cards are logically 70x135 pixels in size
def draw(canvas):
    index = 0
    location_card = 0
    for index in range(len(deck_cards)):
        if exposed[index] == False:
            canvas.draw_polygon([(index * WIDTH_CARD, 0), ((index + 1) * WIDTH_CARD, 0),
                                ((index + 1) * WIDTH_CARD, HEIGHT_CARD), (index * WIDTH_CARD, HEIGHT_CARD)],
                                1, "White", "Steel Blue")
        else:
            canvas.draw_text(str(deck_cards[index]), ((index * WIDTH_CARD) + 14, 115), 60, "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH_CARD * 16, HEIGHT_CARD)
frame.add_button("Reset", new_game, 50)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
