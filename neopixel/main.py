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
def simply_on():

    LED_STRIP.fill(color=Color(0, 0, 0), show=False)
    LED_STRIP.fill_spiral(0, Color(235, 168, 52), show=False)
    LED_STRIP.fill_spiral(1, Color(235, 113, 52), show=False)
    LED_STRIP.fill_spiral(2, Color(235, 201, 52))

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
