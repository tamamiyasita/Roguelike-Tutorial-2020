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

    def sprite_set(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    self.wall = Actor(test_wall, x=x, y=y, color=arcade.color.BLACK, visible_color=COLORS.get(
                        "light_wall"), not_visible_color=COLORS.get("dark_wall"))
                    self.wall.alpha = 0

                    self.sprite_list.append(self.wall)
                elif not self.tiles[x][y].blocked:
                    self.floor = Actor(test_floor, x=x, y=y, color=COLORS.get("transparent"), visible_color=COLORS.get(
                        "light_ground"), not_visible_color=COLORS.get("dark_ground"))
                    self.floor.alpha = 0
                    self.sprite_list.append(self.floor)
