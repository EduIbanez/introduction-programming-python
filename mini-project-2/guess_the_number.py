# Guess the number

# Input will come from buttons and an input field
# all output for the game will be printed in the console

import simpleguitk as simplegui
import random
import math

range_number = 100
remaining_guesses = 0
secret_number = 0

# helper function to start and restart the game
def new_game():
    global secret_number, remaining_guesses
    # initialize global variables used in your code here
    secret_number = random.randrange(0, range_number)
    remaining_guesses = int(math.ceil(math.log(range_number) / math.log(2)))
    print("")
    print("New game. Range is from 0 to " + str(range_number))
    print("Number of remaining guesses is " + str(remaining_guesses))

# define event handlers for control panel
def range100():
    global range_number
    # button that changes the range to [0,100) and starts a new game 
    range_number = 100
    new_game()

def range1000():
    global range_number
    # button that changes the range to [0,1000) and starts a new game     
    range_number = 1000
    new_game()
    
def input_guess(guess):
    global remaining_guesses
    print("")
    print("Guess was " + guess)
    guess = int(guess)
    remaining_guesses -= 1
    print("Number of remaining guesses is " + str(remaining_guesses))
    if guess == secret_number:
        print("Correct!")
        new_game()
    else:
        if remaining_guesses == 0:
            print("You ran out of guesses. The number was " + str(secret_number))
            new_game()
        else:
            if guess > secret_number:
                print("Lower!")
            else:
                print("Higher!")
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 100)
frame.add_button("Range is [0, 1000)", range1000, 100)
frame.add_input("Enter a guess", input_guess, 100)

# call new_game 
new_game()

# start handlers for created frame
frame.start()
