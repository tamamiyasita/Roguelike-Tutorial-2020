from pyglet import sprite
from actor.stairs import Stairs
import arcade
from data import *
from constants import *
from util import grid_to_pixel
from actor.wall import Wall
from actor.floor import Floor
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
        """ 地形スプライトをgame_mapブロック情報から作成する
        """
        map_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == TILE.WALL:
                    wall_number = self.search_wall_number(x, y, self.tiles)

                    wall = Wall(texture_number=wall_number, x=x, y=y,)
                    map_sprites.append(wall)

                elif self.tiles[x][y] == TILE.EMPTY or TILE.STAIRS_DOWN:

                    floor = Floor(texture_number=21, x=x, y=y)
                    map_sprites.append(floor)

                if self.tiles[x][y] == TILE.STAIRS_DOWN:

                    stairs = Stairs(x=x, y=y)
                    map_sprites.append(stairs)

        return map_sprites

    def actor_set(self):
        """actorをgame_mapタイル番号から設定する
        """
        actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.actor_tiles[x][y]) == int:
                    monster_tile_number = get_random_monster_by_challenge(self.actor_tiles[x][y])
                    monster = make_monster_sprite(monster_tile_number)
                    monster.x = x
                    monster.y = y
                    cx, cy = grid_to_pixel(x,y)
                    monster.center_x = cx
                    monster.center_y = cy
                    print(monster.center_x)

                    actor_sprites.append(monster)

        return actor_sprites


    def items_set(self):
        """itemをgame_mapタイル番号から設定する
        """
        item_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.item_tiles[x][y]) == int:
                    item = get_random_items_by_challenge(self.item_tiles[x][y])
                    item.x = x
                    item.y = y
                    cx, cy = grid_to_pixel(x,y)
                    item.center_x = cx
                    item.center_y = cy
                    print(item.center_x)

                    item_sprites.append(item)

        return item_sprites



        # item_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=32)
        # for x in range(self.width):
        #     for y in range(self.height):
        #         if self.item_tiles[x][y] == TILE.HEALING_POTION:
        #             healing_potion = HealingPotion(x, y)
        #             item_sprites.append(healing_potion)
        #         elif self.item_tiles[x][y] == TILE.LIGHTNING_SCROLL:
        #             lightning_scroll = LightningScroll(x, y)
        #             item_sprites.append(lightning_scroll)
        #         elif self.item_tiles[x][y] == TILE.FIREBALL_SCROLL:
        #             fireball_scroll = FireballScroll(x, y)
        #             item_sprites.append(fireball_scroll)

        # return item_sprites

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
