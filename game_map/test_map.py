import arcade
from random import randint, choice

from util import grid_to_pixel

from game_map.door_check import door_check
from constants import *
from data import IMAGE_ID



class TestMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level
        self.PLAYER_POINT = (10,10)

        self.tiles = [[TILE.EMPTY for y in range(height)] for x in range(width)]
        self.actor_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]
        self.item_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]
        self.tiles[width//2][height//2] = TILE.STAIRS_DOWN

    def generate_tile(self):
        pass
