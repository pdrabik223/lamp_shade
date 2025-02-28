from global_variables import ThreadConfig
from led_strip import Color
import utime
import math

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


def delay(sleep_time_s, config: ThreadConfig) -> bool:

    if sleep_time_s < 0.1:
        utime.sleep(sleep_time_s)
        return config.stop_animation

    intervals = int(sleep_time_s / 0.1)
    for _ in range(intervals):
        utime.sleep(0.1)
        if config.stop_animation:
            return True
    utime.sleep(sleep_time_s - (intervals * 0.1))

    return config.stop_animation
