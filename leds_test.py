from gpiozero import LED
from time import sleep

red   = LED(17)
amber = LED(27)
green = LED(22)

for led in (red, amber, green):
    led.on(); sleep(1); led.off()

print("Done.")
