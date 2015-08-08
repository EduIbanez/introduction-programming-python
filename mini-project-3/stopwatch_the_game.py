# Stopwatch: The game

import simpleguitk as simplegui

# define global variables
counter = 0
times_stopped = 0
times_succeed = 0
stopped = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenths_seconds = str(t % 10)
    seconds = str(int((t / 10) % 60))
    minutes = str(int((t / 10) / 60))
    if int(seconds) < 10:
        seconds = str(0) + seconds
    return minutes + ":" + seconds + "." + tenths_seconds

    
# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    global stopped
    timer.start()
    stopped = False

def button_stop():
    global stopped, times_stopped, times_succeed
    timer.stop()
    if stopped == False:
        stopped = True
        times_stopped += 1
        if (counter % 10) == 0:
            times_succeed += 1

def button_reset():
    global stopped, counter, times_stopped, times_succeed
    timer.stop()
    stopped = True
    counter = 0
    times_stopped = 0
    times_succeed = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(counter), (80, 135), 40, "White")
    counter_times = str(times_succeed) + "/" + str(times_stopped)
    canvas.draw_text(counter_times, (235, 50), 20, "Green")

# create frame and timer
frame = simplegui.create_frame("Stopwatch", 300, 200)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button("Start", button_start, 100)
frame.add_button("Stop", button_stop, 100)
frame.add_button("Reset", button_reset, 100)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()
