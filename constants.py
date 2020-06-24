import arcade

TITLE = "Roguelike tutorial 2020"

SPRITE_SIZE = 32
SPRITE_SCALE = 2
MAP_WIDTH = 45
MAP_HEIGHT = 25

SCREEN_WIDTH = int(SPRITE_SIZE * MAP_WIDTH * SPRITE_SCALE)//2
SCREEN_HEIGHT = int(SPRITE_SIZE * MAP_HEIGHT * SPRITE_SCALE)//2

VIEWPORT_MARGIN = 300

MOVE_SPEED = 4

MAX_ROOM = 25
ROOM_MIN_SIZE = 4
ROOM_MAX_SIZE = 8

FOV_ALGO = 0
FOV_LIGHT_WALL = True
FOV_RADIUS = 8

COLORS = {
    "transparent": arcade.color.BLACK,
    "dark_wall": arcade.color.PURPLE_TAUPE,
    "dark_ground": arcade.color.PURPLE_NAVY,
    "light_wall": arcade.color.WHITE,
    "light_ground": arcade.color.WHITE
}

LEFT_FACE = 1
RIGHT_FACE = 2


ACTOR_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
MAP_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
