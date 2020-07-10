from constants import *


def grid_to_pixel(x, y):
    """tilepositionからsprite_sizeに変換する"""
    px = x * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    py = y * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    return px, py


def pixel_to_grid(x, y):
    """sprite_sizeからtile_pixel_to_gridへの位置を指定する"""
    px = x - SPRITE_SIZE // 2 * SPRITE_SCALE
    px = round(px // (SPRITE_SIZE * SPRITE_SCALE))

    py = y - SPRITE_SIZE / 2 * SPRITE_SCALE
    py = round(py // (SPRITE_SIZE * SPRITE_SCALE))
    return px, py
