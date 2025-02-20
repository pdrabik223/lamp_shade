from machine import Pin,  PWM 
import utime
import random




PWM = PWM(Pin(12))
PWM.freq(1000)
current_duty_cycle = 0

def set_duty_cycle(duty_cycle):
    current_duty_cycle = duty_cycle
    PWM.duty_u16(duty_cycle)
    

BUTTON = Pin(15, Pin.IN,Pin.PULL_UP)

animations = []



def animation(f):
    animations.append(f)
    return f

# @animation
# def led_animation_on(animation_duration_s = 2):
  
#     set_duty_cycle(65025)
#     utime.sleep(animation_duration_s)
# @animation
# def led_animation_off(animation_duration_s = 2):
  
#     set_duty_cycle(0)
#     utime.sleep(animation_duration_s)

@animation
def breath(min_brightness= 0.3, max_brightness = 0.9, animation_duration_s = 20):
    
    min_duty_cycle = int(65025 * min_brightness)
    max_duty_cycle = int(65025 * max_brightness)
    
    sleep_time = (animation_duration_s / (max_duty_cycle - min_duty_cycle)) / 2

    for duty in range(min_duty_cycle, max_duty_cycle, 1):
        set_duty_cycle(duty)
        utime.sleep(sleep_time)
        
    for duty in range(max_duty_cycle, min_duty_cycle, -1):
        set_duty_cycle(duty)
        utime.sleep(sleep_time)
        
# @animation
# def fire(min_brightness = 0.2, max_brightness = 0.9, min_animation_duration_s = 0.5, max_animation_duration_s = 6):
    
    
    
    
#     max_duty_cycle = int(65025 * max_brightness) - (current_duty_cycle//4)
#     min_duty_cycle = int(65025 * min_brightness) + (current_duty_cycle//4)
    
#     offset = random.randint(min_duty_cycle, max_duty_cycle)
    
#     next_duty_cycle = current_duty_cycle + offset
    
#     sleep_time = random.random() * (max_animation_duration_s - min_animation_duration_s) + min_animation_duration_s
    
#     if current_duty_cycle < next_duty_cycle:
#         sleep_time = sleep_time / (next_duty_cycle - current_duty_cycle)
#         for duty in range(current_duty_cycle, next_duty_cycle, 1):
#             set_duty_cycle(duty)
#             utime.sleep(sleep_time)
#     else:
#         sleep_time = sleep_time / (current_duty_cycle - next_duty_cycle)
#         for duty in range(next_duty_cycle, current_duty_cycle, -1):
#             set_duty_cycle(duty)
#             utime.sleep(sleep_time)
        
    
    



def main():
    animation_index = 0
    while(True):
        
        if BUTTON.value() == 0:
            animation_index += 1
            if len(animations) == animation_index:
                animation_index = 0
            
        animations[animation_index]()
        
main()
    
    