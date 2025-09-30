from gpiozero import Button
from signal import pause
btn = Button(23, pull_up=True, bounce_time=0.05)  # other side of button wired to GND
btn.when_pressed  = lambda: print("pressed")
btn.when_released = lambda: print("released")
print("Ready. Press the button.")
pause()
