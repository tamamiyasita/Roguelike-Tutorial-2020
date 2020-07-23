import arcade

from constants import *
from actor.actor import Actor
from actor.wall import Wall
from actor.floor import Floor
from actor.orc import Orc
from actor.troll import Troll
from actor.item import Item
from actor.potion import Potion


def map_to_sprites(game_map):

    sprite_list = arcade.SpriteList(
        use_spatial_hash=True, spatial_hash_cell_size=32)

    for y in range(len(game_map[0])):
        for x in range(len(game_map)):
            sprite = None
            if game_map[x][y] == TILE.WALL:
                wall_number = search_wall_number()
                sprite = Wall(texture_number=wall_number, x=x, y=y)

    def search_wall_number(self, x, y, tiles):

        tile_value = set()
        tile_value.add(0)

        if self.width - 1 > x:
            if game_map[x + 1][y].blocked:
                tile_value.add(4)
        if self.height - 1 > y:
            if game_map[x][y + 1].blocked:
                tile_value.add(1)
        if 0 < x:
            if game_map[x - 1][y].blocked:
                tile_value.add(2)
        if 0 < y:
            if game_map[x][y - 1].blocked:
                tile_value.add(8)
        return sum(tile_value)
