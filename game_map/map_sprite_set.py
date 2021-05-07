from actor.map_obj.stairs import Up_Stairs, Down_Stairs
import arcade
from data import IMAGE_ID
from constants import *
from util import grid_to_pixel, pixel_to_grid

from actor.actor import Actor
from actor.map_obj.wall import Wall
from actor.map_obj.floor import Floor
from actor.map_obj.door import DoorH,DoorW

from actor.entities_factory import get_random_monster_by_challenge, get_random_items_by_challenge


class ActorPlacement:
    def __init__(self, game_map, game_engine):
        self.game_map = game_map
        self.tiles = game_map.tiles
        self.actor_tiles = game_map.actor_tiles
        self.item_tiles = game_map.item_tiles
        self.game_engine = game_engine
        self.width = len(self.tiles)
        self.height = len(self.tiles[0])
        # self.my_map = arcade.read_tmx(r"demo\town2.tmx")

    def wall_set(self, image):
        """ 静的な地形スプライトをgame_mapブロック情報から作成する
        """
        wall_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == TILE.WALL:
                    number = self.search_wall_number(x, y, self.tiles)


                    if number == 6 and self.tiles[x][y-1] == TILE.WALL:                    
                        wall = Wall(image=image, texture_number=15, x=x, y=y)
                        wall_sprites.append(wall)
                    else:
                        wall = Wall(image=image, texture_number=number, x=x, y=y)
                        wall_sprites.append(wall)

        return wall_sprites

    def floor_wall(self,image2, number, x, y, floor_sprites):
        if number == 0 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=0, x=x, y=y-1) 
            floor_sprites.append(f_wall)
            
        if number == 1 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W): 
            f_wall = Floor(image=image2, texture_number=1, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 2 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=2, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 3 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=3, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 4 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=4, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 5 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=5, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 6 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=6, x=x, y=y-1) 
            floor_sprites.append(f_wall)

        if number == 7 and self.tiles[x][y-1] in (TILE.EMPTY ,TILE.DOOR_H, TILE.DOOR_W):
            f_wall = Floor(image=image2, texture_number=7, x=x, y=y-1) 
            floor_sprites.append(f_wall)


    def floor_set(self, image=IMAGE_ID["block_floor"], image2=None):
        floor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == TILE.EMPTY or TILE.STAIRS_DOWN or TILE.DOOR:


                    if self.width - 1 > x > 0 and self.height - 2 > y > 0 and self.tiles[x][y+1] != TILE.WALL:

                        floor = Floor(image, x=x, y=y)
                        floor_sprites.append(floor)

                if self.tiles[x][y] == TILE.WALL:
                    number = self.search_wall_number(x, y, self.tiles)
                    self.floor_wall(image2, number, x, y, floor_sprites)


        return floor_sprites


    def search_wall_number(self, x, y, tiles):
        """ 周りのブロック情報からwallテクスチャ番号を計算する関数
        """

        tile_value = set()
        tile_value.add(0)

        if self.width - 1 > x > 0:
            if tiles[x + 1][y] == TILE.WALL:
                tile_value.add(4)

            if tiles[x - 1][y] == TILE.WALL:
                tile_value.add(2)

        if self.height - 1 > y > 0:
            if tiles[x][y + 1] == TILE.WALL:
                tile_value.add(1)

            if tiles[x][y - 1] == TILE.WALL:
                tile_value.add(8)

        return sum(tile_value)


    def tiled_floor_set(self):
        tiled_floor_sprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        floors = arcade.process_layer(
            self.my_map, "floor", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")

        for f in floors:
            x, y = pixel_to_grid(f.center_x, f.center_y)
            floor = Floor(x=x, y=y)
            floor.scale = 2
            floor.texture = f.texture
            floor.color = COLORS.get("dark_ground")
            tiled_floor_sprite.append(floor)

        return tiled_floor_sprite

    def tiled_wall_set(self):
        tiled_wall_sprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        walls = arcade.process_layer(
            self.my_map, "wall", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")

        for w in walls:
            x, y = pixel_to_grid(w.center_x, w.center_y)
            wall = Wall(x=x, y=y)
            wall.scale = 2
            wall.texture = w.texture
            wall.blocks = True
            wall.color = COLORS.get("dark_ground")
            tiled_wall_sprite.append(wall)

        return tiled_wall_sprite

    def tiled_map_obj_set(self):
        tiled_map_obj_sprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        door = arcade.process_layer(
            self.my_map, "door", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")
        up_stairs = arcade.process_layer(
            self.my_map, "up_stairs", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")
        down_stairs = arcade.process_layer(
            self.my_map, "down_stairs", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")

        for m in door:
            x, y = pixel_to_grid(m.center_x, m.center_y)
            obj = DoorH(x=x, y=y)
            obj.scale = 2
            obj.texture = m.texture
            obj.blocks = True
            tiled_map_obj_sprite.append(obj)

        for m in up_stairs:
            x, y = pixel_to_grid(m.center_x, m.center_y)
            obj = Up_Stairs(x=x, y=y)
            obj.scale = 2
            # obj.texture = m.texture
            obj.blocks = True
            tiled_map_obj_sprite.append(obj)

        for m in down_stairs:
            x, y = pixel_to_grid(m.center_x, m.center_y)
            obj = Down_Stairs(x=x, y=y)
            obj.scale = 2
            # obj.texture = m.texture
            obj.blocks = True
            tiled_map_obj_sprite.append(obj)

        return tiled_map_obj_sprite

    def tiled_npc_set(self):
        tiled_npc_sprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        villager_list = arcade.process_layer(
            self.my_map, "villager", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")
        for v in villager_list:
            x, y = pixel_to_grid(v.center_x, v.center_y)
            villager = Villager(x=x, y=y)
            tiled_npc_sprite.append(villager)

        citizen_list = arcade.process_layer(
            self.my_map, "citizen", scaling=2, use_spatial_hash=True, hit_box_algorithm="None")
        for c in citizen_list:
            x, y = pixel_to_grid(c.center_x, c.center_y)
            citizen = Citizen(x=x, y=y)
            tiled_npc_sprite.append(citizen)

        return tiled_npc_sprite

    def map_point_set(self):
        point = None
        map_point_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                # == TILE.EMPTY or TILE.STAIRS_DOWN or TILE.DOOR:
                if self.tiles[x][y] != TILE.WALL and self.tiles[x][y] != TILE.STAIRS_DOWN:

                    point = Actor(image=IMAGE_ID["floor_point"], scale=2, x=x, y=y,
                                  color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])

                    map_point_sprites.append(point)

                elif self.tiles[x][y] == TILE.WALL:# ここでcolorをwhiteにするとマップ全体が見れる
                    point = Actor(image=IMAGE_ID["wall_point"], scale=2, x=x, y=y,
                                  color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])

                    map_point_sprites.append(point)

                elif self.tiles[x][y] == TILE.STAIRS_DOWN:
                    point = Actor(image=IMAGE_ID["stairs_down_point"], scale=2, x=x, y=y,
                                  color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
                if point:
                    map_point_sprites.append(point)

        return map_point_sprites

    def map_obj_set(self):
        """ 動的な地形スプライトをgame_mapブロック情報から作成する
        """
        map_obj_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        for x in range(self.width):
            for y in range(self.height):

                if self.tiles[x][y] == TILE.DOOR_H:

                    door_h = DoorH(x=x, y=y)
                    map_obj_sprites.append(door_h)

                if self.tiles[x][y] == TILE.DOOR_W:

                    door_w = DoorW(x=x, y=y)
                    map_obj_sprites.append(door_w)

                if self.tiles[x][y] == TILE.STAIRS_UP:

                    up_stairs = Up_Stairs(x=x, y=y)
                    map_obj_sprites.append(up_stairs)

                if self.tiles[x][y] == TILE.STAIRS_DOWN:

                    down_stairs = Down_Stairs(x=x, y=y)
                    map_obj_sprites.append(down_stairs)

        return map_obj_sprites

    def actor_set(self):
        """actorをgame_mapタイル番号から設定する
        """
        actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        for x in range(self.width):
            for y in range(self.height):
                if type(self.actor_tiles[x][y]) == int:
                    monster = get_random_monster_by_challenge(
                        self.actor_tiles[x][y])
                    # monster = make_monster_sprite(monster_tile_number)
                    monster.x = x
                    monster.y = y
                    cx, cy = grid_to_pixel(x, y)
                    monster.center_x = cx
                    monster.center_y = cy

                    actor_sprites.append(monster)# ここをコメントアウトすると敵無しに

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

                    item = Actor(image=IMAGE_ID["items_point"], scale=1.2, x=x, y=y,
                                 color=COLORS["black"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["light_ground"])
                    item.x = x
                    item.y = y
                    cx, cy = grid_to_pixel(x, y)
                    item.center_x = cx
                    item.center_y = cy

                    items_point_sprites.append(item)

        return items_point_sprites

