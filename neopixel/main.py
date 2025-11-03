from animation_helpers import delay, rainbow
from led_strip import Color
import _thread
import gc
import random

from global_variables import (
    animations,
    ThreadConfig,
    LED_STRIP,
    button_listener,
)

config = ThreadConfig()


def animation(f):
    animations.append(f)
    return f


@animation
def candle():
    LED_STRIP.brightness(42)
    candle_red = Color(255,0,0)
    candle_orange = Color(200, 80, 0)
    candle_yellow =  Color(180, 100, 0)
    
    LED_STRIP.fill(color=Color(0, 0, 0), show=False)
    LED_STRIP.set_pixels(range(13), candle_red, brightness=255, show=False)
    LED_STRIP.set_pixels(range(13, 26), candle_orange, show=False)
    LED_STRIP.set_pixels(range(26, 41), candle_yellow, brightness=60)
    
    if delay(1, config):
        config.stop_animation = False
        return


@animation
def simply_on():

    LED_STRIP.fill(color=Color(0, 0, 0), show=False)
    LED_STRIP.fill_spiral(0, Color(235/2, 168/2, 52/2), show=False)
    LED_STRIP.fill_spiral(1, Color(235/2, 113/2, 52/2), show=False)
    LED_STRIP.fill_spiral(2, Color(235/2, 201/2, 52/2))

    if delay(1, config):
        config.stop_animation = False
        return


@animation
def simply_off():

    LED_STRIP.fill(color=Color(0, 0, 0))

    if delay(1, config):
        config.stop_animation = False
        return

@animation
def animated_spiral_rainbow():

    colors = [
        rainbow(i, LED_STRIP.size() * 3, third_color=100)
        for i in range(LED_STRIP.size() * 3)
    ]

    for i in range(LED_STRIP.size() * 3):
        LED_STRIP.fill(color=Color(0, 0, 0), show=False)
        LED_STRIP.fill_spiral(0, colors[i], show=False)
        LED_STRIP.fill_spiral(
            1, colors[(i + len(colors) // 3) % len(colors)], show=False
        )
        LED_STRIP.fill_spiral(
            2, colors[(i + (len(colors) // 3) * 2) % len(colors)], show=False
        )
        LED_STRIP.show()
        if delay(0.1, config):
            config.stop_animation = False
            return


@animation
def animated_pastel_rainbow():

    colors = [
        rainbow(i, LED_STRIP.size() * 3, third_color=100)
        for i in range(LED_STRIP.size() * 3)
    ]

    for _ in range(LED_STRIP.size() * 3):

        colors.append(colors.pop(0))

        for i in range(LED_STRIP.size()):
            LED_STRIP.set_pixel(i, colors[i])
        LED_STRIP.show()

        if delay(0.1, config):
            config.stop_animation = False
            return


@animation
def animated_rainbow():

    colors = [rainbow(i, LED_STRIP.size() * 3) for i in range(LED_STRIP.size() * 3)]

    for _ in range(LED_STRIP.size() * 3):

        colors.append(colors.pop(0))

        for i in range(LED_STRIP.size()):
            LED_STRIP.set_pixel(i, colors[i])
        LED_STRIP.show()

        if delay(0.1, config):
            config.stop_animation = False
            return


def main():

    _thread.start_new_thread(button_listener, ([config]))

    while True:
        animations[config.animation_index]()
        print(f"index: {config.animation_index}")
        gc.collect()


if __name__ == "__main__":
    main()
