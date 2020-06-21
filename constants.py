import arcade

TITLE = "Roguelike tutorial 2020"

SPRITE_SIZE = 32
SPRITE_SCALE = 1
MAP_WIDTH = 45
MAP_HEIGHT = 25

SCREEN_WIDTH = int(SPRITE_SIZE * MAP_WIDTH * SPRITE_SCALE)
SCREEN_HEIGHT = int(SPRITE_SIZE * MAP_HEIGHT * SPRITE_SCALE)
MOVE_SPEED = 4

MAX_ROOM = 25
ROOM_MIN_SIZE = 4
ROOM_MAX_SIZE = 8


ACTOR_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
MAP_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
