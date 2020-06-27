import arcade
from data import *
from constants import *
from actor import Actor

test_wall = image.get("test_wall")
test_floor = image.get("test_floor")


class MapSpriteSet:
    def __init__(self, width, height, tiles, floor_img, wall_img):

        self.width = width
        self.height = height
        self.tiles = tiles
        self.sprite_list = MAP_LIST
        self.floor_img = floor_img
        self.wall_img = wall_img
        if self.wall_img[0].width == 16:
            self.scale = SPRITE_SCALE * 2

    def sprite_set(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    wall_number = self.search_wall_number(x, y, self.tiles)

                    self.wall = Actor(image=self.wall_img.get(wall_number), x=x, y=y, blocks=True, scale=self.scale, color=arcade.color.BLACK, visible_color=COLORS.get(
                        "light_wall"), not_visible_color=COLORS.get("dark_wall"))
                    self.wall.alpha = 0

                    self.sprite_list.append(self.wall)
                elif not self.tiles[x][y].blocked:
                    self.floor = Actor(self.floor_img, x=x, y=y, color=COLORS.get("transparent"), visible_color=COLORS.get(
                        "light_ground"), not_visible_color=COLORS.get("dark_ground"))
                    self.floor.alpha = 0
                    self.sprite_list.append(self.floor)

    def search_wall_number(self, x, y, tiles):

        tile_value = set()
        tile_value.add(0)

        if self.width - 1 > x:
            if self.tiles[x + 1][y].blocked:
                tile_value.add(4)
        if self.height - 1 > y:
            if self.tiles[x][y + 1].blocked:
                tile_value.add(1)
        if 0 < x:
            if self.tiles[x - 1][y].blocked:
                tile_value.add(2)
        if 0 < y:
            if self.tiles[x][y - 1].blocked:
                tile_value.add(8)
        return sum(tile_value)
