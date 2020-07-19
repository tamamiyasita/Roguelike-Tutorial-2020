import arcade
from arcade.key import T
from data import *
from constants import *
from actor.actor import Actor
from actor.wall import Wall
from actor.floor import Floor

# test_wall = image.get("test_wall")
# test_floor = image.get("test_floor")


class MapSpriteSet:
    def __init__(self, tiles):

        self.tiles = tiles
        self.width = len(tiles[0])
        self.height = len(tiles)
        self.map_sprits = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        # if self.wall_img[0].width <= 17:
        #     self.scale = SPRITE_SCALE * 2

    def actor_set(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    wall_number = self.search_wall_number(x, y, self.tiles)

                    wall = Wall(texture_number=wall_number, x=x, y=y,)
                    self.map_sprits.append(wall)

                elif not self.tiles[x][y].blocked:
      
                    floor = Floor(texture_number=21, x=x, y=y)
                    self.map_sprits.append(floor)
        
        return self.map_sprits
        

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
