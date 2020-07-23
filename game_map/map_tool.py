import arcade
from constants import *


def initialize_tiles(width, height):
    tiles = [[Tile(TILE.WALL) for y in range(height)]
             for x in range(width)]

    return tiles


def actor_tiles(width, height):
    actor_tiles = [[Tile(TILE.EMPTY) for y in range(height)]
                   for x in range(width)]
    return actor_tiles


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if not block_sight:
            block_sight = blocked
        self.block_sight = block_sight


def is_blocked(tiles, x, y):
    try:
        if tiles[x][y].blocked:
            return True

        return False
    except:
        pass


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
