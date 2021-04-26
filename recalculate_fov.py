"""視野の計算"""

from math import radians
import arcade
import math

from arcade import sprite_list

from constants import *
from util import grid_to_pixel
from actor.damage_pop import DamagePop


def recalculate_fov(engine, radius):
    """ Fovの計算を行う
    """
    player = engine.player
    char_x, char_y  = player.position_xy
    sprite_lists = [engine.cur_level.wall_sprites, engine.cur_level.floor_sprites, 
                    engine.cur_level.actor_sprites, engine.cur_level.item_sprites,
                    engine.cur_level.map_obj_sprites, engine.cur_level.map_point_sprites,
                    engine.cur_level.item_point_sprites]
    



    # 最初に渡された全てのスプライトリストをループし、is_visible等をFalseにして画面から隠す
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.is_visible = False
                sprite.color = sprite.not_visible_color
                if Tag.npc in sprite.tag:
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
                    if hasattr(sprite.ai, "visible_check"):
                        if sprite.ai.visible_check == False:
                            engine.damage_pop.append(DamagePop("！", (250,240,0), sprite, 15, size=30))
                            engine.move_switch = False
                            sprite.ai.visible_check = True

            if blocks:
                break
    
    # 全てのスプライトを再度ループし、is_visibleがTrueなら画面に表示する
    for sprite_list in sprite_lists:
        for sprite in sprite_list:
            if sprite.is_visible:
                sprite.color = sprite.visible_color
                sprite.alpha = 255
