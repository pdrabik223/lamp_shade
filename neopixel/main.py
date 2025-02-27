from neopixel import Neopixel
import utime
import random
from machine import Pin
import utime
import random
import _thread


button_a = Pin(22, Pin.IN, Pin.PULL_UP)
button_b  = Pin(21, Pin.IN, Pin.PULL_UP)
button_c  = Pin(2, Pin.IN, Pin.PULL_UP)



numpix = 41
strip = Neopixel(numpix, 0, 3, "GRBW")


red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
pink = (200, 0, 100)
violet = (50, 0, 100)
white = (200, 255, 200)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

delay = 0.5
strip.brightness(255)
blank = (0,0,0)


 

strip.fill(red)
strip.show()
        
while True:
    if button_a.value() == 0:
        print("button_a")
    if button_b.value() == 0:
        print("button_b")    
    if button_c.value() == 0:
        print("button_c")
    utime.sleep(0.1)