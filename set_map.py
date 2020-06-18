import arcade
from util import map_position, pixel_position


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if not block_sight:
            block_sight = blocked
        self.block_sight = block_sight


class SetMap:
    def __init__(self, width, height, sprite_list):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.sprite_list = sprite_list
        self.sprite_set()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)]
                 for x in range(self.width)]

        tiles[5][5].blocked = True
        tiles[6][5].blocked = True
        tiles[6][6].blocked = True

        return tiles

    def is_blocked(self, x, y):
        try:
            if self.tiles[x][y].blocked:
                return True

            return False
        except:
            pass

    def sprite_set(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    px, py = pixel_position(x, y)
                    wall = arcade.Sprite(
                        r"image/wall.png", center_x=px, center_y=py)
                    self.sprite_list.append(wall)
                elif not self.tiles[x][y].blocked:
                    px, py = pixel_position(x, y)
                    floor = arcade.Sprite(
                        r"image/floor.jpg", center_x=px, center_y=py)
                    self.sprite_list.append(floor)
