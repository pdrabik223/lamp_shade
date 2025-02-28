import utime
from led_strip import LedStrip
from machine import Pin


LED_STRIP = LedStrip()

BUTTON_A = Pin(22, Pin.IN, Pin.PULL_UP)
BUTTON_B = Pin(21, Pin.IN, Pin.PULL_UP)
BUTTON_C = Pin(2, Pin.IN, Pin.PULL_UP)


animations = []


class ThreadConfig:
    stop_animation = False
    animation_index = 0


def button_listener(config: ThreadConfig):

    a: bool = False
    b: bool = False
    c: bool = False

    while True:
        a = BUTTON_A.value() == 0
        b = BUTTON_B.value() == 0
        c = BUTTON_C.value() == 0

        if a and b and c:
            print(f"all")

        elif a or b or c:
            config.animation_index += 1
            if len(animations) == config.animation_index:
                config.animation_index = 0
            config.stop_animation = True
            print(f"any,  index: {config.animation_index}")
            utime.sleep(0.5)

        utime.sleep(0.1)
