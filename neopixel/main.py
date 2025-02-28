from neopixel import Neopixel
import utime
from machine import Pin
import _thread
import gc
import math
import random


class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self, r: float, g: float, b: float):
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255

        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    def to_tuple(self):
        return (self.r, self.g, self.b)

    @staticmethod
    def red():
        return Color(255, 0, 0)

    @staticmethod
    def orange():
        return Color(255, 50, 0)

    @staticmethod
    def yellow():
        return Color(255, 100, 0)

    @staticmethod
    def green():
        return Color(0, 255, 0)

    @staticmethod
    def blue():
        return Color(0, 0, 255)

    @staticmethod
    def indigo():
        return Color(100, 0, 90)

    @staticmethod
    def pink():
        return Color(200, 0, 100)

    @staticmethod
    def violet():
        return Color(50, 0, 100)

    @staticmethod
    def white():
        return Color(200, 255, 200)

    @staticmethod
    def black():
        return Color(0, 0, 0)


BUTTON_A = Pin(22, Pin.IN, Pin.PULL_UP)
BUTTON_B = Pin(21, Pin.IN, Pin.PULL_UP)
BUTTON_C = Pin(2, Pin.IN, Pin.PULL_UP)

stop_animation = False
animation_index = 0
animations = []


class LedStrip:
    _led_strip = Neopixel(41, 0, 3, "GRB")

    def __init__(self) -> None:
        self._led_strip.brightness(42)
        self._led_strip.fill(Color.red().to_tuple())
        self._led_strip.show()

    def fill(self, color: Color, show: bool = True):
        self._led_strip.fill(color.to_tuple())
        if show:
            self._led_strip.show()

    def fill_spiral(self, spiral: int, color: Color, show: bool = True):
        assert 0 <= spiral <= 3

        for i in range(41):
            if i % 3 == spiral:
                self._led_strip.set_pixel(i, color.to_tuple())
        if show:
            self._led_strip.show()

    def set_pixels(self, indexes, color: Color, show: bool = True):
        for index in indexes:
            self._led_strip.set_pixel(index, color.to_tuple())
        if show:
            self._led_strip.show()

    def set_pixel(self, index: int, color: Color, show: bool = True):
        self._led_strip.set_pixel(index, color.to_tuple())
        if show:
            self._led_strip.show()

    def show(self):
        self._led_strip.show()

    def brightness(self, brightness: int, show: bool = True):
        self._led_strip.brightness(brightness)
        if show:
            self._led_strip.show()

    @staticmethod
    def size():
        return 41


LED_STRIP = LedStrip()


def animation(f):
    animations.append(f)
    return f

def rainbow(id: int, max_id: int, brightness: int = 255, third_color: int = 0) -> Color:

    # // sine wave algorithm
    # // 3 parts
    # // 1 :
    # // r = cos(i) , g = sin(i), b =0
    # // 2 :
    # // r = 0 , g = cos(i), b = sin(x)
    # // 3:
    # // r = sin(i) , g = 0, b = cos(x)
    # // every part is max_height / 3 translates into 0, PI/2

    # // so for example in point 1/3 * max_height
    # // r = cos(PI/2) = 0, g = sin(PI/2) = 1, b = 0
    witch_third = id // (max_id / 3)

    if witch_third == 0:
        height_in_radians = id * math.pi / (max_id // 3) / 2

        return Color(
            math.cos(height_in_radians) * brightness,
            math.sin(height_in_radians) * brightness,
            third_color,
        )
    if witch_third == 1:

        id -= max_id // 3
        height_in_radians = id * math.pi / (max_id // 3) / 2
        return Color(
            third_color,
            math.cos(height_in_radians) * brightness,
            math.sin(height_in_radians) * brightness,
        )

    if witch_third == 2:

        id -= 2 * max_id // 3
        height_in_radians = id * math.pi / (max_id // 3) / 2
        return Color(
            math.sin(height_in_radians) * brightness,
            third_color,
            math.cos(height_in_radians) * brightness,
        )

    return Color.red()


@animation
def simply_on():
    global stop_animation
    LED_STRIP.fill(color=Color(0, 0, 0), show=False)
    LED_STRIP.fill_spiral(0, Color(235, 168, 52), show=False)
    LED_STRIP.fill_spiral(1, Color(235, 113, 52), show=False)
    LED_STRIP.fill_spiral(2, Color(235, 201, 52))

    if delay(1):
        stop_animation = False
        return


@animation
def animated_spiral_rainbow():
    global stop_animation

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
        if delay(0.1):
            stop_animation = False
            return


@animation
def animated_pastel_rainbow():
    global stop_animation

    colors = [
        rainbow(i, LED_STRIP.size() * 3, third_color=100)
        for i in range(LED_STRIP.size() * 3)
    ]

    for _ in range(LED_STRIP.size() * 3):

        colors.append(colors.pop(0))

        for i in range(LED_STRIP.size()):
            LED_STRIP.set_pixel(i, colors[i])
        LED_STRIP.show()

        if delay(0.1):
            stop_animation = False
            return


@animation
def animated_rainbow():
    global stop_animation

    colors = [rainbow(i, LED_STRIP.size() * 3) for i in range(LED_STRIP.size() * 3)]

    for _ in range(LED_STRIP.size() * 3):

        colors.append(colors.pop(0))

        for i in range(LED_STRIP.size()):
            LED_STRIP.set_pixel(i, colors[i])
        LED_STRIP.show()

        if delay(0.1):
            stop_animation = False
            return


def button_listener():
    global animation_index
    global animations
    global stop_animation
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
            animation_index += 1
            if len(animations) == animation_index:
                animation_index = 0
            stop_animation = True
            print(f"any,  index: {animation_index}")
            utime.sleep(0.5)

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


def set_color(brightness: int, duration_s):
    LED_STRIP.brightness(brightness)
    LED_STRIP.fill(Color(255, 0, 0))
    return delay(duration_s)


def gradient_color_shift(animation_steps, animation_duration_s):
    for duty in animation_steps:
        if set_color(duty, animation_duration_s / len(animation_steps)):
            return


def get_random_small_float(offset: float = 0):
    return random.uniform(-0.1, 0.1) + offset


def quick_bling():

    min_duty_cycle = int(255 * get_random_small_float(0.3))
    max_duty_cycle = int(255 * get_random_small_float(0.8))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(20, 30))
    gradient_color_shift(animation_steps, 0)


def stable_oscillation():
    min_duty_cycle = int(255 * get_random_small_float(0.4))
    max_duty_cycle = int(255 * get_random_small_float(0.7))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2, 8))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float() * 2))

    animation_steps = range(max_duty_cycle, min_duty_cycle, random.randint(-8, -2))
    gradient_color_shift(animation_steps, 2 + (get_random_small_float() * 2))


def stabilization(offset: float = 0):
    min_duty_cycle = int(255 * (0.6 + offset))
    max_duty_cycle = int(255 * (0.9 + offset))

    animation_steps = range(min_duty_cycle, max_duty_cycle, random.randint(2, 8))
    gradient_color_shift(animation_steps, 3)

    animation_steps = range(max_duty_cycle, min_duty_cycle, random.randint(-8, -2))
    gradient_color_shift(animation_steps, 3)


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
