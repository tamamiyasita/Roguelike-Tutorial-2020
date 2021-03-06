from os import name
from pyglet import sprite
from actor.stairs import Up_Stairs
import arcade
from data import *
from constants import *
from util import grid_to_pixel, pixel_to_grid

from actor.actor import Actor
from actor.wall import Wall
from actor.floor import Floor
from actor.door import Door

from actor.entities_factory import get_random_monster_by_challenge, get_random_items_by_challenge
from actor.entities_factory import make_monster_sprite

from actor.healing_potion import HealingPotion
from actor.lightning_scroll import LightningScroll
from actor.fireball_scroll import FireballScroll


class ActorPlacement:
    def __init__(self, game_map, game_engine):
        self.game_map = game_map
        self.tiles = game_map.tiles
        self.actor_tiles = game_map.actor_tiles
        self.item_tiles = game_map.item_tiles
        self.game_engine = game_engine
        self.width = len(self.tiles)
        self.height = len(self.tiles[0])

    def map_set(self):
        """ 静的な地形スプライトをgame_mapブロック情報から作成する
        """
        wall_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == TILE.WALL:
                    wall_number = self.search_wall_number(x, y, self.tiles)

                    wall = Wall(texture_number=wall_number, x=x, y=y,)
                    wall_sprites.append(wall)

                elif self.tiles[x][y] == TILE.EMPTY or TILE.STAIRS_DOWN or TILE.DOOR:

                    floor = Floor(texture_number=21, x=x, y=y)
                    wall_sprites.append(floor)

                if self.tiles[x][y] == TILE.STAIRS_DOWN:

                    stairs = Up_Stairs(x=x, y=y)
                    wall_sprites.append(stairs)

        return wall_sprites

    def tiled_floor_set(self):
        tiled_floor_sprite =  arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        my_map = arcade.read_tmx("demo\m_test.tmx")

        floors = arcade.process_layer(my_map, "floor",scaling=4, use_spatial_hash=True, hit_box_algorithm="None")

        for f in floors:
            x, y = pixel_to_grid(f.center_x, f.center_y)
            floor = Floor(x=x, y=y)
            floor.scale = 4
            floor.texture = f.texture
            tiled_floor_sprite.append(floor)


        return tiled_floor_sprite
            


    def tiled_wall_set(self):
        tiled_wall_sprite =  arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        my_map = arcade.read_tmx("demo\m_test.tmx")

        walls = arcade.process_layer(my_map, "wall",scaling=4, use_spatial_hash=True, hit_box_algorithm="None")

        for w in walls:
            x, y = pixel_to_grid(w.center_x, w.center_y)
            wall = Wall(x=x, y=y)
            wall.scale = 4
            wall.texture = w.texture
            wall.blocks = True
            tiled_wall_sprite.append(wall)



        return tiled_wall_sprite


    def map_point_set(self):
        map_point_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                # == TILE.EMPTY or TILE.STAIRS_DOWN or TILE.DOOR:
                if self.tiles[x][y] != TILE.WALL:

                    point = Actor(name="floor_point", scale=2, x=x, y=y,
                                  color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
                    map_point_sprites.append(point)

                elif self.tiles[x][y] == TILE.WALL:
                    point = Actor(name="wall_point", scale=2, x=x, y=y,
                                  color=COLORS["white"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
                    map_point_sprites.append(point)

        return map_point_sprites

    def map_obj_set(self):
        """ 動的な地形スプライトをgame_mapブロック情報から作成する
        """
        map_obj_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):

                if self.tiles[x][y] == TILE.DOOR:

                    door = Door(x=x, y=y)
                    map_obj_sprites.append(door)

        return map_obj_sprites

    def actor_set(self):
        """actorをgame_mapタイル番号から設定する
        """
        actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.actor_tiles[x][y]) == int:
                    monster_tile_number = get_random_monster_by_challenge(
                        self.actor_tiles[x][y])
                    monster = make_monster_sprite(monster_tile_number)
                    monster.x = x
                    monster.y = y
                    cx, cy = grid_to_pixel(x, y)
                    monster.center_x = cx
                    monster.center_y = cy

                    # actor_sprites.append(monster)

        return actor_sprites

    def items_set(self):
        """itemをgame_mapタイル番号から設定する
        """
        item_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.item_tiles[x][y]) is int:
                    item = get_random_items_by_challenge(self.item_tiles[x][y])

                    item.x = x
                    item.y = y
                    cx, cy = grid_to_pixel(x, y)
                    item.center_x = cx
                    item.center_y = cy

                    item_sprites.append(item)

        return item_sprites

    def items_point_set(self):
        items_point_sprites = arcade.SpriteList(
            use_spatial_hash=False, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.item_tiles[x][y]) is int:

                    item = Actor(name="items_point", scale=1.2, x=x, y=y,
                                 color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
                    item.x = x
                    item.y = y
                    cx, cy = grid_to_pixel(x, y)
                    item.center_x = cx
                    item.center_y = cy

                    items_point_sprites.append(item)

        return items_point_sprites

    def search_wall_number(self, x, y, tiles):
        """ 周りのブロック情報からwallテクスチャ番号を計算する関数
        """

        tile_value = set()
        tile_value.add(0)

        if self.width - 1 > x:
            if self.tiles[x + 1][y] == TILE.WALL:
                tile_value.add(4)
        if self.height - 1 > y:
            if self.tiles[x][y + 1] == TILE.WALL:
                tile_value.add(1)
        if 0 < x:
            if self.tiles[x - 1][y] == TILE.WALL:
                tile_value.add(2)
        if 0 < y:
            if self.tiles[x][y - 1] == TILE.WALL:
                tile_value.add(8)
        return sum(tile_value)
