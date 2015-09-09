# Memory - Images

import simpleguitk as simplegui
import random

WIDTH_CARD = 110
HEIGHT_CARD = 160

# helper function to initialize globals
def new_game():
    global deck_cards, exposed, state, turns
    characters = [catelyn_tully, cersei_lannister, daenerys_targaryen, eddard_stark, jaime_lannister, joffrey_baratheon, jon_snow, loras_tyrell, lysa_tully,
               margaery_tyrell, oberyn_martell, renly_baratheon, robb_stark, robert_baratheon, sansa_stark, stannis_baratheon, tommen_baratheon, tyrion_lannister]
    characters = characters + characters
    random.shuffle(characters)
    deck_cards = [characters[:9], characters[9:18], characters[18:27], characters[27:]]
    state = 0
    turns = 0
    exposed = [[], [], [], []]
    for index in range(4):
        for number in range(9):
            exposed[index].append(False)
    label.set_text("Turns = " + str(turns))

# define event handlers
def mouseclick(pos):
    global state, first_choice, second_choice, turns
    position = (pos[0] // WIDTH_CARD, pos[1] // HEIGHT_CARD)
    if state == 0:        
        exposed[position[1]][position[0]] = True
        first_choice = position
        state = 1
    elif state == 1:
        if exposed[position[1]][position[0]] == False:
            exposed[position[1]][position[0]] = True
            second_choice = position
            state = 2
            turns += 1
            label.set_text("Turns = " + str(turns))
    else:
        if exposed[position[1]][position[0]] == False:
            if deck_cards[first_choice[1]][first_choice[0]] != deck_cards[second_choice[1]][second_choice[0]]:
                exposed[first_choice[1]][first_choice[0]] = False
                exposed[second_choice[1]][second_choice[0]] = False
            exposed[position[1]][position[0]] = True
            first_choice = position
            state = 1

# cards are logically 110x160 pixels in size
def draw(canvas):
    index_y = 0
    location_card_y = 0
    for list_cards in deck_cards:
        index_x = 0
        location_card_x = 0
        for card in list_cards:
            if exposed[index_y][index_x] == False:
                canvas.draw_image(game_thrones, (412 / 2, 564 / 2), (412, 564),
                                  ((WIDTH_CARD / 2) + location_card_x, (HEIGHT_CARD / 2) + location_card_y), (WIDTH_CARD, HEIGHT_CARD))
            else:
                canvas.draw_image(card, (412 / 2, 564 / 2), (412, 564),
                                  ((WIDTH_CARD / 2) + location_card_x, (HEIGHT_CARD / 2) + location_card_y), (WIDTH_CARD, HEIGHT_CARD))
            index_x += 1
            location_card_x += WIDTH_CARD
        index_y += 1
        location_card_y += HEIGHT_CARD

# load images
game_thrones = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/game_thrones.jpg")
catelyn_tully = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/catelyn_tully.jpg")
cersei_lannister = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/cersei_lannister.jpg")
daenerys_targaryen = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/daenerys_targaryen.jpg")
eddard_stark = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/eddard_stark.jpg")
jaime_lannister = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/jaime_lannister.jpg")
joffrey_baratheon = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/joffrey_baratheon.jpg")
jon_snow = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/jon_snow.jpg")
loras_tyrell = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/loras_tyrell.jpg")
lysa_tully = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/lysa_tully.jpg")
margaery_tyrell = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/margaery_tyrell.jpg")
oberyn_martell = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/oberyn_martell.jpg")
renly_baratheon = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/renly_baratheon.jpg")
robb_stark = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/robb_stark.jpg")
robert_baratheon = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/robert_baratheon.jpg")
sansa_stark = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/sansa_stark.jpg")
stannis_baratheon = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/stannis_baratheon.jpg")
tommen_baratheon = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/tommen_baratheon.jpg")
tyrion_lannister = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-5/images/tyrion_lannister.jpg")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH_CARD * 9, HEIGHT_CARD * 4)
frame.add_button("Reset", new_game, 50)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
