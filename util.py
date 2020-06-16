from constants import *

def pixel_tile(x, y):
    """tilepositionからsprite_sizeに変換する"""
    px = x * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    py = y * SPRITE_SIZE * SPRITE_SCALE + SPRITE_SIZE // 2 * SPRITE_SCALE
    return px, py


def map_position(x, y):
    """sprite_sizeからtile_map_positionへの位置を指定する"""
    px = x - SPRITE_SIZE // 2 * SPRITE_SCALE
    px = round(px // (SPRITE_SIZE * SPRITE_SCALE))

    py = y - SPRITE_SIZE / 2 * SPRITE_SCALE
    py = round(py // (SPRITE_SIZE * SPRITE_SCALE))
    return px, py