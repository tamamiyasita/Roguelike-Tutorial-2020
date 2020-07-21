import arcade
from arcade.key import T
from data import *
from constants import *
from actor.actor import Actor
from actor.wall import Wall
from actor.floor import Floor
from actor.orc import Orc
from actor.troll import Troll
from actor.potion import Potion
from actor.lightning_scroll import LightningScroll

# test_wall = image.get("test_wall")
# test_floor = image.get("test_floor")


class MapobjPlacement:
    def __init__(self, game_map, game_engine):
        self.game_map = game_map
        self.tiles = game_map.tiles
        self.game_engine = game_engine
        self.actor_tiles = game_map.actor_tiles
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)

    def map_set(self):
        map_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    wall_number = self.search_wall_number(x, y, self.tiles)

                    wall = Wall(texture_number=wall_number, x=x, y=y,)
                    map_sprites.append(wall)

                elif not self.tiles[x][y].blocked:

                    floor = Floor(texture_number=21, x=x, y=y)
                    map_sprites.append(floor)

        return map_sprites

    def actor_set(self):
        actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if self.actor_tiles[x][y] == TILE_ORC:
                    orc = Orc(x, y)
                    actor_sprites.append(orc)
                elif self.actor_tiles[x][y] == TILE_TROLL:
                    troll = Troll(x, y)
                    actor_sprites.append(troll)

        return actor_sprites

    def items_set(self):
        item_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if self.actor_tiles[x][y] == TILE_HEALING_POTION:
                    potion = Potion(x, y)
                    item_sprites.append(potion)
                elif self.actor_tiles[x][y] == TILE_LIGHTNING_SCROLL:
                    l_scroll = LightningScroll(x, y)
                    item_sprites.append(l_scroll)

        return item_sprites
    # def place_entities(self, room, max_monsters_per_room, max_items_per_room):
    #     number_of_monsters = randint(0, max_monsters_per_room)
    #     number_of_items = randint(0, max_items_per_room)

    #     for i in range(number_of_monsters):
    #         x = randint(room.x1 + 1, room.x2 - 1)
    #         y = randint(room.y1 + 1, room.y2 - 1)

    #         if not any([actor for actor in actor_list if actor.x == x and actor.y == y]):
    #             if randint(0, 100) < 80:
    #                 Orc(x, y, game_map=self)

    #             else:
    #                 Troll(x, y, game_map=self)
    #     for i in range(number_of_items):
    #         x = randint(room.x1 + 1, room.x2 - 1)
    #         y = randint(room.y1 + 1, room.y2 - 1)

    #         if not any([actor for actor in actor_list if actor.x == x and actor.y == y]):
    #             type = randint(0, 100)
    #             if type < 40:
    #                 Potion(x=x, y=y)
    #             elif type < 67:
    #                 LightningScroll(x=x, y=y)
    #             else:
    #                 FireballScroll(x=x, y=y)

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
