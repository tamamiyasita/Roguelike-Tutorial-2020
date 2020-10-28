import arcade
from enum import Enum, auto

from arcade.key import ESCAPE


TITLE = "Roguelike tutorial 2020"

SPRITE_SIZE = 32
SPRITE_SCALE = 2

GRID_SIZE = SPRITE_SIZE * SPRITE_SCALE

MAP_WIDTH = 40
MAP_HEIGHT = 35

GAME_GROUND_WIDTH = int(GRID_SIZE * MAP_WIDTH)
GAME_GROUND_HEIGHT = int(GRID_SIZE * MAP_HEIGHT)

STATES_PANEL_WIDTH = int(GRID_SIZE * 4)
STATES_PANEL_HEIGHT = int(GRID_SIZE * 2)

SCREEN_WIDTH = int(GRID_SIZE * 23)
SCREEN_HEIGHT = int(GRID_SIZE * 15)

MAIN_PANEL_X = int(SCREEN_WIDTH - STATES_PANEL_WIDTH)
MAIN_PANEL_Y = int(SCREEN_HEIGHT - STATES_PANEL_HEIGHT)

VIEWPORT_MARGIN = int(((SCREEN_WIDTH-STATES_PANEL_WIDTH) /
                       2 + (SCREEN_HEIGHT-STATES_PANEL_HEIGHT) / 2)/2)

MOVE_SPEED = 9

EXPERIENCE_PER_LEVEL = [10, 800, 1300, 2000]

FOV_ALGO = 0
FOV_LIGHT_WALL = True
FOV_RADIUS = 6
DEATH_DELAY = 0.5

DEFAULT_SPEED = 7
DEFAULT_ATTACK_SPEED = 6


class Tag(Enum):
    # items
    item = auto()
    flower = auto()
    used = auto()
    equip = auto()
    skill = auto()
    active = auto()

    # chara
    player = auto()
    npc = auto()
    enemy = auto()
    pet = auto()
    friendly = auto()
    quest = auto()

    # obj
    map_obj = auto()
    wall = auto()
    floor = auto()
    door = auto()
    stairs = auto()

    free = auto()


COLORS = {
    "black": arcade.color.BLACK,
    "white": arcade.color.WHITE,
    "dead": arcade.color.GRAY_BLUE,
    "dark_wall": arcade.color.PURPLE_TAUPE,
    "dark_ground": arcade.color.PURPLE_NAVY,
    "light_wall": arcade.color.WHITE_SMOKE,
    "light_ground": arcade.color.WHITE_SMOKE,
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
    LOOK = auto()
    SELECT_LOCATION = auto()
    CHARACTER_SCREEN = auto()
    INVENTORY = auto()
    MESSAGE_WINDOW = auto()
    DELAY_WINDOW = auto()
    LOAD_WINDOW = auto()
    LEVEL_UP_WINDOW = auto()


class state(Enum):
    READY = auto()
    DELAY = auto()
    ON_MOVE = auto()
    TURN_END = auto()
    ATTACK = auto()
    FOV = auto()
    DOOR = auto()
    AMOUNT = auto()


class NPC_state(Enum):
    REQUEST = auto()
    WAITING = auto()
    REWARD = auto()
    NORMAL = auto()
