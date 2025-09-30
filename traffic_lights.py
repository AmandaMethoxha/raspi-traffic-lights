from gpiozero import LED, Button
from time import sleep

# LEDs (BCM)
red   = LED(17)
amber = LED(27)
green = LED(22)

# Button on GPIO23 to GND, internal pull-up
btn = Button(23, pull_up=True, bounce_time=0.05)

# Timings (seconds)
T_GREEN = 6
T_AMBER = 2
T_RED = 6
T_RED_AMBER = 2
T_PED_EXTRA = 3   # extra red time if pressed during red

ped_request = False
def on_press():
    global ped_request
    ped_request = True
    print("Pedestrian requested")

btn.when_pressed = on_press

def go_green_with_early_exit():
    global ped_request
    green.on()
    for _ in range(T_GREEN):   # check once per second
        sleep(1)
        if ped_request:        # leave green early if requested
            break
    green.off()

def amber_phase():
    amber.on(); sleep(T_AMBER); amber.off()

def red_phase():
    global ped_request
    red.on()
    if ped_request:
        sleep(T_RED + T_PED_EXTRA)  # extend red once
        ped_request = False
    else:
        sleep(T_RED)
    red.off()

def red_amber_phase():
    amber.on(); sleep(T_RED_AMBER); amber.off()

while True:
    red_amber_phase()          # RED+AMBER → GREEN
    go_green_with_early_exit() # GREEN (can be shortened by button)
    amber_phase()              # AMBER
    red_phase()                # RED (serve/extend if requested)

