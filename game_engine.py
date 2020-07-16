
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
from game_map.basic_dungeon import BasicDungeon
from game_map.map_sprite_set import MapSpriteSet
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
        self.actor_list = None
        self.player = None
        self.crab = None
        self.actor_list = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=3)
        self.selected_item = None
        self.turn_check = None
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.actor_list = ACTOR_LIST
        self.map_list = MAP_LIST
        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)

        self.fov_recompute = True


        self.player = Player(
            self.game_map.player_pos[0], self.game_map.player_pos[1], game_map=self.game_map, inventory=Inventory(capacity=5))

        self.crab = Crab(self.player.x+2, self.player.y, self.game_map)
        self.cnf = ConfusionScroll(
            self.player.x+1, self.player.y)

        self.fov_map = initialize_fov(self.game_map)
        self.mapsprite = MapSpriteSet(
            MAP_WIDTH, MAP_HEIGHT, self.game_map.tiles, floors.get(0), wall_3)
        self.mapsprite.sprite_set()

        viewport(self.player)

    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}

    def get_dict(self):
        # player_dict = self.get_actor_dict(self.player)

        dungeon_dict = []
        for sprite in MAP_LIST:
            dungeon_dict.append(self.get_actor_dict(sprite))

        actor_dict = []
        for sprite in ACTOR_LIST:
            actor_dict.append(self.get_actor_dict(sprite))

        result = {#"player": player_dict,
                   "dungeon":dungeon_dict,
                   "actor":actor_dict}

        return result

    def restore_from_dict(self, data):
        # global MAP_LIST, ENTITY_LIST

        self.map_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        self.actor_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        # player_dict = data["Player"]
        # self.player.restore_from_dict(player_dict["Player"])

        for actor_dict in data["dungeon"]:
            actor_name = list(actor_dict.keys())[0]
            if actor_name == "Actor":
                actor = Actor()
                actor.restore_from_dict(actor_dict[actor_name])
                self.map_list.append(actor)

            actor = restore_actor(actor_dict)

        

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
                self.turn_check = self.move_enemies()

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
                    (self.player.center_x, self.player.center_y), ITEM_LIST)
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
                        ITEM_LIST.append(item)
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

    def move_enemies(self):
        turn_check = "next_turn"
        for actor in ACTOR_LIST:
            if actor.ai and not actor.is_dead:
                results = actor.ai.take_turn(
                    target=self.player, game_map=self.game_map, sprite_lists=[ACTOR_LIST])
                if results:
                    self.action_queue.extend(results)
                # else:
                #     results = actor.ai.take_turn(
                #         target=self.player, game_map=self.game_map, sprite_lists=[MAP_LIST])
                #     if results:
                #         self.action_queue.extend(results)

                turn_check = actor
        return turn_check

    def fov(self):
        recompute_fov(self.fov_map, self.player.x, self.player.y,
                      FOV_RADIUS, FOV_LIGHT_WALL, FOV_ALGO)
        fov_get(self.game_map, self.fov_map)
        self.fov_recompute = False

    def view(self):
        if self.player.state == state.ON_MOVE:
            viewport(self.player)

    def turn_change(self, delta_time):
        turn = 0

        if self.player.state == state.TURN_END:
            self.player.state = state.DELAY
            self.action_queue.extend([{"enemy_turn": True}])
        # elif self.turn_check == "next_turn" or self.turn_check.state == state.TURN_END:
        elif self.turn_check == "next_turn":
            self.turn_check = None
            self.action_queue.extend([{"player_turn": True}])

        elif self.turn_check:
            for actor in ACTOR_LIST:
                if actor.ai:
                    if actor.state == state.TURN_END:
                        turn += 1
                    if turn == len(ACTOR_LIST) - 1:
                        self.action_queue.extend([{"player_turn": True}])
                        self.turn_check = None
