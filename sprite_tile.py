from data import *
from actor import Actor


def sprite_tile(map_tile):
    for x in range(map_tile.width):
        for y in range(map_tile.height):
            if not map_tile.tiles[x][y].blocked:
                floor = Actor(r"image/wall.png", )
