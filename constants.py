import arcade
from enum import Enum, auto

from arcade.key import ESCAPE


TITLE = "Roguelike tutorial 2020"

SPRITE_SIZE = 32
SPRITE_SCALE = 2

MAP_WIDTH = 35
MAP_HEIGHT = 25

STATES_PANEL_HEIGHT = 80

SCREEN_WIDTH = int(SPRITE_SIZE * MAP_WIDTH * SPRITE_SCALE)//SPRITE_SCALE
SCREEN_HEIGHT = int(SPRITE_SIZE * MAP_HEIGHT *
                    SPRITE_SCALE)//SPRITE_SCALE + STATES_PANEL_HEIGHT

VIEWPORT_MARGIN = 300

MOVE_SPEED = 6

EXPERIENCE_PER_LEVEL = [150, 800, 1300, 2000]

FOV_ALGO = 0
FOV_LIGHT_WALL = True
FOV_RADIUS = 8
DEATH_DELAY = 0.5

COLORS = {
    "transparent": arcade.color.BLACK,
    "dark_wall": arcade.color.PURPLE_TAUPE,
    "dark_ground": arcade.color.PURPLE_NAVY,
    "light_wall": arcade.color.WHITE,
    "light_ground": arcade.color.WHITE,
    "status_panel_background": arcade.color.PINK_LACE,
    "status_panel_text": arcade.color.BLACK,
    "status_bar_background": arcade.color.PINK_LACE,
    "status_bar_foreground": arcade.color.RED_DEVIL
}


class TILE:
    EMPTY = False
    WALL = True
    STAIRS_DOWN = auto()

    ORC = auto()
    TROLL = auto()
    
    HEALING_POTION = auto()
    LIGHTNING_SCROLL = auto()
    FIREBALL_SCROLL = auto()
    CONFUSION_SCROLL = auto()


class GAME_STATE(Enum):
    NORMAL = auto()
    SELECT_LOCATION = auto()
    CHARACTER_SCREEN = auto()
    DELAY_WINDOW = auto()


class state(Enum):
    READY = auto()
    DELAY = auto()
    ON_MOVE = auto()
    TURN_END = auto()
    ATTACK = auto()
    FOV = auto()


KEYMAP_UP = [arcade.key.UP, arcade.key.W, arcade.key.NUM_8]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.S, arcade.key.NUM_2]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.A, arcade.key.NUM_4]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.D, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.Q, arcade.key.NUM_7, arcade.key.HOME]
KEYMAP_UP_RIGHT = [arcade.key.E, arcade.key.NUM_9, arcade.key.PAGEUP]
KEYMAP_DOWN_LEFT = [arcade.key.Z, arcade.key.NUM_1, arcade.key.END]
KEYMAP_DOWN_RIGHT = [arcade.key.X, arcade.key.NUM_3, arcade.key.PAGEDOWN]
KEYMAP_REST = [arcade.key.R]
KEYMAP_PICKUP = [arcade.key.G, arcade.key.NUM_5]
KEYMAP_SELECT_ITEM_1 = [arcade.key.KEY_1]
KEYMAP_SELECT_ITEM_2 = [arcade.key.KEY_2]
KEYMAP_SELECT_ITEM_3 = [arcade.key.KEY_3]
KEYMAP_SELECT_ITEM_4 = [arcade.key.KEY_4]
KEYMAP_SELECT_ITEM_5 = [arcade.key.KEY_5]
KEYMAP_SELECT_ITEM_6 = [arcade.key.KEY_6]
KEYMAP_SELECT_ITEM_7 = [arcade.key.KEY_7]
KEYMAP_SELECT_ITEM_8 = [arcade.key.KEY_8]
KEYMAP_SELECT_ITEM_9 = [arcade.key.KEY_9]
KEYMAP_SELECT_ITEM_0 = [arcade.key.KEY_0]
KEYMAP_USE_ITEM = [arcade.key.U]
KEYMAP_DROP_ITEM = [arcade.key.H]
KEYMAP_CHARACTER_SCREEN = [arcade.key.C]
KEYMAP_USE_STAIRS = [arcade.key.ENTER]
KEYMAP_CANCEL = [arcade.key.ESCAPE]

