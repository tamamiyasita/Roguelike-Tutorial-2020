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
    DOOR = auto()
    STAIRS_DOWN = auto()

    ORC = auto()
    TROLL = auto()
    
    LONG_SWORD = auto()
    WOOD_BUCKLER = auto()

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


