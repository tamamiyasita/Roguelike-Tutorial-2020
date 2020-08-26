"""視野の計算"""

from data import player
from math import radians
import arcade
import math

from arcade import sprite_list

from constants import *
from util import grid_to_pixel


def recalculate_fov(char_x, char_y, radius, sprite_lists):
    """ Fovの計算を行う
    """



    # 最初に渡された全てのスプライトリストをループし、is_visible等をFalseにして画面から隠す
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.not_visible_color
                if sprite.ai:
                    sprite.alpha = 0
    
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
            y2 = round(y2)

            pixel_point = grid_to_pixel(x2, y2)

            blocks = False
            for sprite_list in sprite_lists:
                sprites_at_point = arcade.get_sprites_at_exact_point(pixel_point, sprite_list)

                # 探索済みならis_visibleをTrueにする
                for sprite in sprites_at_point:
                    sprite.is_visible = True
                    if sprite.block_sight:
                        blocks = True

            if blocks:
                break
    
    # 全てのスプライトを再度ループし、is_visibleがTrueなら画面に表示する
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.color = sprite.visible_color
                sprite.alpha = 255

