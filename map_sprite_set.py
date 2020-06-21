import arcade
from data import *
from constants import *
from actor import Actor

test_wall = image.get("test_wall")
test_floor = image.get("test_floor")


class MapSpriteSet:
    def __init__(self, width, height, tiles):

        self.width = width
        self.height = height
        self.tiles = tiles
        self.sprite_list = MAP_LIST

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    wall = Actor(test_wall, x, y)

                    self.sprite_list.append(wall)
                elif not self.tiles[x][y].blocked:
                    floor = Actor(test_floor, x, y)

                    self.sprite_list.append(floor)
