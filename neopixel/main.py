from neopixel import Neopixel
import utime
import random
from machine import Pin
import utime
import random
import _thread
import gc

class Color:
    red = (255, 0, 0)
    orange = (255, 50, 0)
    yellow = (255, 100, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    indigo = (100, 0, 90)
    pink = (200, 0, 100)
    violet = (50, 0, 100)  
    white = (200, 255, 200)
    black = (0,0,0)

    

BUTTON_A = Pin(22, Pin.IN, Pin.PULL_UP)
BUTTON_B = Pin(21, Pin.IN, Pin.PULL_UP)
BUTTON_C = Pin(2, Pin.IN, Pin.PULL_UP)

LED_STRIP = Neopixel(41, 0, 3, "GRB")
LED_STRIP.brightness(255)
LED_STRIP.fill(Color.red)
     
animation_index = 0
animations = []

def animation(f):
    animations.append(f)
    return f

@animation
def simply_on(color:Color = Color.red):
    LED_STRIP.fill(color)
    LED_STRIP.show()
    utime.sleep(1)

def button_listener():
    global animation_index
    global animations
    
    a:bool = False
    b:bool = False
    c:bool = False
    
    while True:
        a =  BUTTON_A.value() == 0
        b =  BUTTON_A.value() == 0
        c =  BUTTON_A.value() == 0
        
        if (a or b or c) :
            animation_index += 1
            if len(animations) == animation_index:
                animation_index = 0
            print("any")
            
        if (a and b and c):
            animation_index += 1
            if len(animations) == animation_index:
                animation_index = 0
            print("all")           
    
        utime.sleep(0.1)



def delay(sleep_time_s) -> bool:
    global stop_animation
    if sleep_time_s < 0.1:
        utime.sleep(sleep_time_s)
        return stop_animation

    intervals = int(sleep_time_s / 0.1)
    for _ in range(intervals):
        utime.sleep(0.1)
        if stop_animation:
            return True
    utime.sleep(sleep_time_s - (intervals * 0.1))

    return stop_animation

def set_brightness(duty_cycle, sleep_time_s, color:Color = Color.white) -> bool:
    LED_STRIP.fill(color, duty_cycle)
    LED_STRIP.show()
    return delay(sleep_time_s)

def gradient_color_shift(animation_steps, animation_duration_s):
    for duty in animation_steps:
        if set_brightness(duty, animation_duration_s / len(animation_steps)):
            return

def get_random_small_float(offset=0):
    return random.uniform(-0.1, 0.1) + offset


def quick_bling():
    min_duty_cycle = int(65535 * get_random_small_float(0.3))
    max_duty_cycle = int(65535 * get_random_small_float(0.8))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(20, 30))
    gradient_color_shift(animation_steps, 0)


def stable_oscillation():
    min_duty_cycle = int(65535 * get_random_small_float(0.4))
    max_duty_cycle = int(65535 * get_random_small_float(0.7))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2, 8))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float() * 2))

    animation_steps = range(max_duty_cycle, min_duty_cycle, random.randint(-8, -2))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float() * 2))


def stabilization(offset=0):
    min_duty_cycle = int(65535 * (0.6 + offset))
    max_duty_cycle = int(65535 * (0.9 + offset))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2, 8))
    gradient_color_shift(animation_steps, 3)

    animation_steps = range(max_duty_cycle, min_duty_cycle, random.randint(-8, -2))
    gradient_color_shift(animation_steps, 3)


@animation
def small_candle():

    for _ in range(random.randint(4, 7)):
        stable_oscillation()  # candle is "flowing" from left to right in a semi stable way

    for _ in range(random.randint(4, 8)):
        quick_bling()  # flame is flickering quickly and dynamically


@animation
def big_candle():

    for _ in range(random.randint(4, 7)):
        stable_oscillation()  # candle is "flowing" from left to right in a semi stable way

    for _ in range(random.randint(4, 8)):
        quick_bling()  # flame is flickering quickly and dynamically

    for _ in range(random.randint(4, 7)):
        stable_oscillation()  # back to stable oscillation

    if random.random() > 0.5:
        for _ in range(random.randint(8, 16)):
            stabilization()  # candle moves slowly is in stable state
    else:
        for _ in range(random.randint(8, 16)):
            stabilization(
                -0.2
            )  # candle moves slowly is in stable state, but is dimmer overall


    
def main():
    global animation_index
    global animations

    _thread.start_new_thread(button_listener, ())

    while True:
        animations[animation_index]()
        gc.collect()





if __name__ == "__main__":
    main()
