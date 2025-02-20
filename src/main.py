from machine import Pin,  PWM 
import utime
import random
import _thread
import gc

BUTTON = Pin(15, Pin.IN,Pin.PULL_UP)
PWM = PWM(Pin(12))
PWM.freq(1000)


stop_animation = False
animation_index = 0
animations = []


def set_brightness(duty_cycle, sleep_time_s)->bool:
    set_duty_cycle(duty_cycle)
    return delay(sleep_time_s)


def set_duty_cycle(duty_cycle):
    if duty_cycle > 65535:
        raise ValueError(f"Duty cycle must be less than 65535, current: {duty_cycle}")
    if duty_cycle < 0:
        raise ValueError(f"Duty cycle must be bigger than 0, current: {duty_cycle}")
    PWM.duty_u16(duty_cycle)

def delay(sleep_time_s) -> bool:
    global stop_animation
    if (sleep_time_s < 0.1):
        utime.sleep(sleep_time_s)
        return stop_animation
    
    intervals = int(sleep_time_s / 0.1)
    for i in range(intervals):
        utime.sleep(0.1)
        if stop_animation:
            return True
    utime.sleep(sleep_time_s - (intervals * 0.1))
    
    return stop_animation


def animation(f):
    animations.append(f)
    return f


@animation
def simply_on():
  
    set_duty_cycle(65535)
    delay(10)

def gradient_color_shift(animation_steps, animation_duration_s):
     for duty in animation_steps:
        if set_brightness(duty, animation_duration_s / len(animation_steps)):
            return

@animation
def breeze(min_brightness= 0.3, max_brightness = 0.9, animation_duration_s = 10):
    
    min_duty_cycle = int(65535 * min_brightness)
    max_duty_cycle = int(65535 * max_brightness)
    
    animation_duration_s /= 2 # animation is divided into two parts  
   
    animation_steps = range(min_duty_cycle, max_duty_cycle, 10)
    gradient_color_shift(animation_steps, animation_duration_s)
    
    animation_steps = range(max_duty_cycle, min_duty_cycle, -10)
    gradient_color_shift(animation_steps, animation_duration_s)


def get_random_small_float():
    return random.uniform(-0.1, 0.1)

def quick_bling():
    # global current_duty_cycle
    
    min_duty_cycle = int(65535 * (0.3 + get_random_small_float()))
    max_duty_cycle = int(65535 * (0.8 + get_random_small_float()))
    
    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(20,30))
    gradient_color_shift(animation_steps, 0)

def stable_oscillation():
    min_duty_cycle = int(65535 * (0.4+ get_random_small_float()))
    max_duty_cycle = int(65535 * (0.8+ get_random_small_float()))
    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(5,10))
    gradient_color_shift(animation_steps, 0.1)

    animation_steps = range(max_duty_cycle, min_duty_cycle, -1*random.randint(5,10))
    gradient_color_shift(animation_steps, 0.1)



def stabilization():
    min_duty_cycle = int(65535 * (0.4+ get_random_small_float()))
    max_duty_cycle = int(65535 * (0.7+ get_random_small_float()))
    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2,8))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float()*2))
    
    animation_steps = range(max_duty_cycle, min_duty_cycle, -1*random.randint(2,8))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float()*2))

def stabilization2(offset = 0):
    min_duty_cycle = int(65535 * (0.6 + offset))
    max_duty_cycle = int(65535 * (0.9 + offset))
    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2,8))
    gradient_color_shift(animation_steps, 3)
    
    animation_steps = range(max_duty_cycle, min_duty_cycle, -1*random.randint(2,8))
    gradient_color_shift(animation_steps, 3)

    
@animation
def small_candle():
   
    for i in range( random.randint(4,7)):
        stabilization()
   
    for i in range( random.randint(4,8)):
        quick_bling()

  
@animation
def big_candle():
   
    for i in range( random.randint(4,7)):
        stabilization()
   
    for i in range( random.randint(4,8)):
        quick_bling()
    
    for i in range( random.randint(4,7)):
        stabilization()
    
    if random.random() > 0.5:
        for i in range( random.randint(8,16)):
            stabilization2()
    else:
        for i in range( random.randint(8,16)):
            stabilization2(-0.2)
            
               
@animation
def simply_off():
  
    set_duty_cycle(0)
    delay(10)
     
def button_listener(sleep_time = 0.1):
    global animation_index
    global stop_animation
    global animations
    
    while(True):
        if BUTTON.value() == 0:
            stop_animation = True
            animation_index += 1
            if len(animations) == animation_index:
                animation_index = 0
            utime.sleep(sleep_time*2)
            
        utime.sleep(sleep_time)    


def main():
    global animation_index
    global stop_animation
    global animations
    
    _thread.start_new_thread(button_listener, ())
    
    while(True):
        if stop_animation:
            stop_animation = False
            set_duty_cycle(0)
            utime.sleep(0.2)

        animations[animation_index]()
        gc.collect()
    
if __name__ == "__main__":
    main()
    
    