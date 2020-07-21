
from actor.inventory import Inventory
from collections import deque

import arcade
# import tcod

from actor.actor import Actor
from actor.inventory import Inventory
# from actor.ai import Basicmonster
from constants import *
from data import *
# from actor.fighter import Fighter
from fov_functions import fov_get, initialize_fov, recompute_fov
# from recalculate_fov import recalculate_fov
from game_map.basic_dungeon import BasicDungeon
from game_map.map_sprite_set import MapobjPlacement
# from actor.item import Item
# from actor.potion import Potion
from actor.confusion_scroll import ConfusionScroll
from viewport import viewport
from actor.PC import Player
from actor.Crab import Crab
# from util import grid_to_pixel, pixel_to_grid
from actor.restore_actor import restore_actor


class GameEngine:
    def __init__(self):
        self.chara_sprites = None
        self.actor_sprites = None
        self.map_sprites = None
        self.item_sprites = None
        self.player = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=3)
        self.selected_item = None
        self.turn_check = None
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []

    def setup(self):
        self.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)
        mapsprite = MapobjPlacement(self.game_map, self).map_set()
        actorsprite = MapobjPlacement(self.game_map, self).actor_set()
        itemsprite = MapobjPlacement(self.game_map, self).items_set()
        self.map_sprites = mapsprite
        self.actor_sprites = actorsprite
        self.item_sprites = itemsprite

        self.fov_recompute = True

        self.player = Player(
            self.game_map.player_pos[0], self.game_map.player_pos[1], inventory=Inventory(capacity=5))
        self.chara_sprites.append(self.player)
        # self.crab = Crab(self.player.x + 2, self.player.y +
        #                  1, game_engine=self,)
        # self.actor_sprites.append(self.crab)
        # self.cnf = ConfusionScroll(
        #     self.player.x+1, self.player.y)

        self.fov_map = initialize_fov(self.game_map)

        viewport(self.player)

        arcade.set_background_color(arcade.color.BLACK)

    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}

    def get_dict(self):
        player_dict = self.get_actor_dict(self.player)

        actor_dict = []
        for sprite in self.actor_sprites:
            actor_dict.append(self.get_actor_dict(sprite))

        dungeon_dict = []
        for sprite in self.map_sprites:
            dungeon_dict.append(self.get_actor_dict(sprite))

        result = {"player": player_dict,
                  "actor": actor_dict,
                  "dungeon": dungeon_dict}
        return result

    def restore_from_dict(self, data):

        self.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.map_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        player_dict = data["player"]
        self.player.restore_from_dict(player_dict["Player"])
        # player = restore_actor(player_dict)
        self.chara_sprites.append(self.player)

        # for actor_dict in data["actor"]:
        #     self.crab.restore_from_dict(actor_dict["Crab"])
        #     self.actor_sprites.append(self.crab)

        for actor_dict in data["actor"]:
            actor = restore_actor(actor_dict)
            self.actor_sprites.append(actor)

        for dungeon_dict in data["dungeon"]:
            maps = restore_actor(dungeon_dict)
            self.map_sprites.append(maps)
    ###アクションキュー###

    def process_action_queue(self, delta_time):
        new_action_queue = []
        for action in self.action_queue:
            if "player_turn" in action:
                print("player_turn")
                self.player.state = state.READY
                self.fov()

            if "enemy_turn" in action:
                print("enemy_turn")
                # self.turn_checkにターン終了フラグを入れる
                self.turn_check = self.move_enemies(self.player)

            if "message" in action:
                print("Message")
                self.messages.append(action["message"])

            if "dead" in action:
                print("Death")
                target = action["dead"]
                target.color = arcade.color.GRAY_BLUE
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "player has died!"}])
                else:
                    self.game_map.tiles[target.x][target.y].blocked = False
                    new_action_queue.extend(
                        [{"message": f"{target.name} has been killed!"}])
                    new_action_queue.extend(
                        [{"delay": {"time": DEATH_DELAY, "action": {"remove": target}}}])
            if "remove" in action:
                target = action["remove"]
                target.remove_from_sprite_lists()

            if "pass" in action:
                target = action["pass"]
                target.state = state.TURN_END

            if "delay" in action:
                target = action["delay"]
                target["time"] -= delta_time
                if target["time"] > 0:
                    new_action_queue.extend([{"delay": target}])
                else:
                    new_action_queue.extend([target["action"]])

            if "pickup" in action:
                actors = arcade.get_sprites_at_exact_point(
                    (self.player.center_x, self.player.center_y), self.item_sprites)
                for actor in actors:
                    if actor.item:
                        results = self.player.inventory.add_item(actor)
                        if results:
                            new_action_queue.extend(results)

            if "select_item" in action:
                item_number = action["select_item"]
                if 1 <= item_number <= self.player.inventory.capacity:
                    if self.selected_item != item_number - 1:
                        self.selected_item = item_number - 1

            if "use_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        results = item.use(self)
                        if results:
                            new_action_queue.extend(results)
                            self.player.state = state.TURN_END

            if "drop_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        self.player.inventory.remove_item_number(item_number)
                        self.actor_sprites.append(item)
                        item.center_x = self.player.center_x
                        item.center_y = self.player.center_y
                        new_action_queue.extend(
                            [{"message": f"You dropped the {item.name}"}])

        self.action_queue = new_action_queue
    #####################

    def grid_click(self, grid_x, grid_y):
        for f in self.grid_select_handlers:
            results = f(grid_x, grid_y)
            if results:
                self.action_queue.extend(results)
        self.grid_select_handlers = []

    def move_enemies(self, target):
        turn_check = "next_turn"
        for actor in self.actor_sprites:
            if actor.ai and not actor.is_dead:
                results = actor.ai.take_turn(
                    target=target, game_map=self.game_map, sprite_lists=[self.map_sprites, self.actor_sprites])
                if results:
                    self.action_queue.extend(results)

                # else:
                #     results = actor.ai.take_turn(
                #         target=self.player, game_map=self.game_map, sprite_lists=[MAP_LIST])
                #     if results:
                #         self.action_queue.extend(results)

                turn_check = actor
        print(turn_check)
        return turn_check

    def fov(self):
        if self.fov_recompute == True:
            # recalculate_fov(self.player.x, self.player.y, FOV_RADIUS,[self.map_sprites, self.actor_sprites])
            recompute_fov(self.fov_map, self.player.x, self.player.y,
                          FOV_RADIUS, FOV_LIGHT_WALL, FOV_ALGO)
            fov_get(self.game_map, self.fov_map,
                    self.actor_sprites, self.map_sprites, self.item_sprites)
        self.fov_recompute = False

    def view(self):
        if self.player.state == state.ON_MOVE:
            viewport(self.player)

    def turn_change(self, delta_time):
        turn = 0
        mons = 0

        if self.player.state == state.TURN_END:
            self.player.state = state.DELAY
            self.action_queue.extend([{"enemy_turn": True}])
        # elif self.turn_check == "next_turn" or self.turn_check.state == state.TURN_END:
        elif self.turn_check == "next_turn":
            self.turn_check = None
            self.action_queue.extend([{"player_turn": True}])

        elif self.turn_check:
            for actor in self.actor_sprites:
                print("actor_?")
                if actor.ai:
                    if actor.state == state.TURN_END:
                        turn += 1
                        print(turn)
                    if turn == len(self.actor_sprites):
                        self.action_queue.extend([{"player_turn": True}])
                        self.turn_check = None
