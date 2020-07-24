"""視野の計算"""

from math import radians
import arcade
import math

from arcade import sprite_list

from constants import *
from util import grid_to_pixel


def recalculate_fov(char_x, char_y, radius, sprite_lists):
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.not_visible_color
                sprite.alpha = sprite.alpha / 2
    
    resolution = 12
    circumference = 2 * math.pi * radius

    radians_per_point = 2 * math.pi / (circumference * resolution)
    point_count = int(round(circumference)) * resolution
    for i in range(point_count):
        radians = i * radians_per_point

        x = math.sin(radians) * radius + char_x
        y = math.cos(radians) * radius + char_y

        ray_checks = radius
        for j in range(ray_checks):
            v1 = char_x, char_y
            v2 = x, y
            x2, y2 = arcade.lerp_vec(v1, v2, j / ray_checks)
            x2 = round(x2)

