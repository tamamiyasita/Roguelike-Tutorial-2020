import arcade
import tcod

from constants import *
from util import pixel_position


def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(
                fov_map, x, y, not game_map.tiles[x][y].block_sight, not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)


def fov_get(game_map, fov_map):
    for y in range(game_map.height):
        for x in range(game_map.width):
            visible = tcod.map_is_in_fov(fov_map, x, y)
            if not visible:
                point = pixel_position(x, y)
                sprite_point = arcade.get_sprites_at_exact_point(
                    point, ENTITY_LIST)
                for sprite in sprite_point:
                    sprite.is_visible = False

            elif visible:
                point = pixel_position(x, y)
                sprite_point = arcade.get_sprites_at_exact_point(
                    point, ENTITY_LIST)
                for sprite in sprite_point:
                    sprite.is_visible = True
                    sprite.alpha = 255
            for sprite in ACTOR_LIST:
                if not tcod.map_is_in_fov(fov_map, sprite.x, sprite.y):
                    sprite.alpha = 0
                else:
                    sprite.alpha = 255

    for sprite in ENTITY_LIST:
        if sprite.is_visible:
            sprite.color = sprite.visible_color

        else:
            sprite.color = sprite.not_visible_color
