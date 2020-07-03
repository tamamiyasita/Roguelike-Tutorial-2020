import arcade
from enum import Enum, auto


TITLE = "Roguelike tutorial 2020"

SPRITE_SIZE = 32
SPRITE_SCALE = 1
MAP_WIDTH = 45
MAP_HEIGHT = 25

SCREEN_WIDTH = int(SPRITE_SIZE * MAP_WIDTH * SPRITE_SCALE)//SPRITE_SCALE
SCREEN_HEIGHT = int(SPRITE_SIZE * MAP_HEIGHT * SPRITE_SCALE)//SPRITE_SCALE

VIEWPORT_MARGIN = 300

MOVE_SPEED = 4

MAX_ROOM = 25
ROOM_MIN_SIZE = 4
ROOM_MAX_SIZE = 8

FOV_ALGO = 0
FOV_LIGHT_WALL = True
FOV_RADIUS = 8
DEATH_DELAY = 0.5

COLORS = {
    "transparent": arcade.color.BLACK,
    "dark_wall": arcade.color.PURPLE_TAUPE,
    "dark_ground": arcade.color.PURPLE_NAVY,
    "light_wall": arcade.color.WHITE,
    "light_ground": arcade.color.WHITE
}

LEFT_FACE = 1
RIGHT_FACE = 2


class state(Enum):
    READY = auto()
    DELAY = auto()
    MOVE_END = auto()


ACTOR_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
MAP_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)
ENTITY_LIST = arcade.SpriteList(
    use_spatial_hash=True, spatial_hash_cell_size=32)


KEYMAP_UP = [arcade.key.UP, arcade.key.W, arcade.key.NUM_8]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.S, arcade.key.NUM_2]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.A, arcade.key.NUM_4]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.D, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.Q, arcade.key.NUM_7, arcade.key.HOME]
KEYMAP_UP_RIGHT = [arcade.key.E, arcade.key.NUM_9, arcade.key.PAGEUP]
KEYMAP_DOWN_LEFT = [arcade.key.Z, arcade.key.NUM_1, arcade.key.END]
KEYMAP_DOWN_RIGHT = [arcade.key.X, arcade.key.NUM_3, arcade.key.PAGEDOWN]
