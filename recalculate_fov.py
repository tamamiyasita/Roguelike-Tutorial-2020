from math import radians
from typing import List

import arcade
import math


from constants import *
from actor.actor import Actor
from util import grid_to_pixel

def recalculate_fov(cx:int, cy:int, radius:int, sprite_lists):
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.not_visible_color
                sprite.alpha = 100

    resolution = 12
    circumference = 2 * math.pi * radius

    radians_per_point = 2 * math.pi / (circumference * resolution)
    point_count = int(round(circumference)) * resolution
    for i in range(point_count):
        radians = i * radians_per_point

        x = math.sin(radians) * radius + cx
        y = math.cos(radians) * radius + cy

        raychecks = radius
        for j in range(raychecks):
            v1 = cx, cy
            v2 = x, y
            x2, y2 = arcade.lerp_vec(v1, v2, j / raychecks)
            x2 = round(x2)
            y2 = round(y2)

            pixel_point = grid_to_pixel(x2, y2)

            blocks = False
            for sprite_list in sprite_lists:
                sprites_at_point = arcade.get_sprites_at_exact_point(
                    pixel_point, sprite_list
                )

                for sprite in sprites_at_point:
                    sprite.is_visible = True
                    if sprite.block_sight:
                        blocks = True
            if blocks:
                break
        
        for sprite_list in sprite_lists:
            for sprite in sprite_list:
                if sprite.is_visible:
                    sprite.color = sprite.visible_color
                    sprite.alpha = 100
