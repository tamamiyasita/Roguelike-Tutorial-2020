
import arcade
import tcod
from collections import deque

from constants import *
from data import *
from inventory import Inventory
from actor import Actor
from basic_dungeon import BasicDungeon
from fighter import Fighter
from fov_functions import initialize_fov, recompute_fov, fov_get
from viewport import viewport
from map_sprite_set import MapSpriteSet
from fighter import Fighter
from ai import Basicmonster
from item import Item
from potion import Potion


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

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.actor_list = ACTOR_LIST
        self.map_list = MAP_LIST
        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)

        self.fov_recompute = True
        fighter_component = Fighter(hp=30, defense=2, power=5)
        fighter_component2 = Fighter(hp=3, defense=2, power=5)
        ai_component = Basicmonster()

        self.player = Actor(image["player"], "player", self.game_map.player_pos[0], self.game_map.player_pos[1],
                            blocks=False, inventory=Inventory(capacity=5),
                            fighter=fighter_component,
                            sub_img=image.get("player_move"), map_tile=self.game_map)
        self.player.state = state.READY

        # self.item = Potion(
        #     image=potion[0], name="Healing Potion", x=self.player.x+1, y=self.player.y+1, blocks=False, color=COLORS.get("transparent"), visible_color=COLORS.get(
        #         "light_ground"), not_visible_color=COLORS.get("dark_ground"), item=Item())
        # self.item.alpha = 0

        self.crab = Actor(image["crab"], "crab", self.player.x+2, self.player.y,
                          blocks=True, fighter=fighter_component2, ai=ai_component,
                          scale=SPRITE_SCALE * 0.5, sub_img=True, map_tile=self.game_map)

        self.actor_list.append(self.player)
        self.actor_list.append(self.crab)
        # ITEM_LIST.append(self.item)

        self.fov_map = initialize_fov(self.game_map)
        self.mapsprite = MapSpriteSet(
            MAP_WIDTH, MAP_HEIGHT, self.game_map.tiles, floors.get(0), wall_3)
        self.mapsprite.sprite_set()

        viewport(self.player)
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

    def move_enemies(self):
        turn_check = "next_turn"
        for actor in ACTOR_LIST:
            if actor.ai and not actor.is_dead:
                results = actor.ai.take_turn(
                    #     target=self.player, game_map=self.game_map, sprite_lists=[MAP_LIST, ACTOR_LIST])
                    # if results:
                    #     self.action_queue.extend(results)
                    # else:
                    #     results = actor.ai.take_turn(
                    target=self.player, game_map=self.game_map, sprite_lists=[MAP_LIST])
                if results:
                    self.action_queue.extend(results)

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

    def turn_change(self):
        if self.player.state == state.TURN_END:
            self.player.state = state.DELAY
            self.action_queue.extend([{"enemy_turn": True}])
            # self.turn_check = self.move_enemies()
        elif self.turn_check:
            if self.turn_check == "next_turn" or self.turn_check.state == state.TURN_END:
                self.turn_check = None
                self.action_queue.extend([{"player_turn": True}])
                # self.player.state = state.READY
                # self.fov()
