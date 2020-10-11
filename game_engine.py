
import arcade
from collections import deque

from constants import *
from data import *
from game_map.basic_dungeon import BasicDungeon
from game_map.town_map import TownMap
from game_map.map_sprite_set import ActorPlacement
from recalculate_fov import recalculate_fov

from actor.inventory import Inventory
from actor.item_point_check import ItemPoint
from actor.characters.PC import Player
from actor.map_obj.stairs import Stairs
from actor.restore_actor import restore_actor
from util import get_door, get_blocking_entity
from turn_loop import TurnLoop
from fire import Fire
from actor.items.boomerang import Boomerang
from actor.damage_pop import Damagepop

from actor.items.short_sword import ShortSword
from actor.items.long_sword import LongSword
from actor.items.confusion_scroll import ConfusionScroll
from actor.items.fireball_scroll import FireballScroll
from actor.items.small_shield import SmallShield
from actor.items.healing_potion import HealingPotion
from actor.items.cirsium import Cirsium


class GameLevel:
    """dungeon階層毎にsprite_listを生成する"""

    def __init__(self):
        self.chara_sprites = None
        self.actor_sprites = None
        self.floor_sprites = None
        self.wall_sprites = None
        self.map_point_sprites = None
        self.item_sprites = None
        self.item_pointe_sprites = None
        self.equip_sprites = None
        self.effect_sprites = None
        self.map_obj_sprites = None

        self.level = 0


class GameEngine:
    def __init__(self):
        self.stories = []  # 階層を格納する変数
        self.cur_level = None

        self.player = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=6)
        self.selected_item = None  # キー押下で直接選択したアイテム
        self.turn_check = []
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []
        self.move_switch = True
        self.damage_pop = []
        self.messenger = None

        self.player = Player(
            inventory=Inventory(capacity=5))
        # self.f = F()
        # self.player.equipment.item_slot["head"] = self.f

    def setup_level(self, level_number):
        """開始レベル(階層)によってmapを変更する"""

        self.map_width, self.map_height = MAP_WIDTH, MAP_HEIGHT
        self.game_level = GameLevel()
        self.level = level_number
        if self.level == 0:
            return self.start_town_init()
        if self.level >= 1:
            return self.basic_dungeon_init(self.player)

    def start_town_init(self):
        # self.town_map = [[TILE.EMPTY for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
        self.town_map = TownMap(
            self.map_width, self.map_height, self.level, self.player)
        """ スプライトリストの初期化 """
        floor_sprite = ActorPlacement(self.town_map, self).tiled_floor_set()
        wall_sprite = ActorPlacement(self.town_map, self).tiled_wall_set()
        map_point_sprite = ActorPlacement(self.town_map, self).map_point_set()
        map_obj_sprite = ActorPlacement(
            self.town_map, self).tiled_map_obj_set()
        actorsprite = ActorPlacement(self.town_map, self).tiled_npc_set()
        itemsprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        items_point_sprite = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.game_level.floor_sprites = floor_sprite
        self.game_level.wall_sprites = wall_sprite
        self.game_level.map_point_sprites = map_point_sprite
        self.game_level.map_obj_sprites = map_obj_sprite
        self.game_level.actor_sprites = actorsprite
        self.game_level.item_sprites = itemsprite
        self.game_level.item_point_sprites = items_point_sprite
        self.game_level.equip_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.game_level.effect_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.game_level.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.game_level.chara_sprites.append(self.player)

        self.short_sword = ShortSword(self.player.x+1, self.player.y + 1)
        self.game_level.item_sprites.append(self.short_sword)

        self.game_level.level = self.level

        return self.game_level

    def basic_dungeon_init(self, player):

        self.game_map = BasicDungeon(
            self.map_width, self.map_height, self.level, player)

        """ スプライトリストの初期化 """
        floor_sprite = ActorPlacement(self.game_map, self).floor_set()
        wall_sprite = ActorPlacement(self.game_map, self).wall_set()
        map_point_sprite = ActorPlacement(self.game_map, self).map_point_set()
        map_obj_sprite = ActorPlacement(self.game_map, self).map_obj_set()
        actorsprite = ActorPlacement(self.game_map, self).actor_set()
        itemsprite = ActorPlacement(self.game_map, self).items_set()
        items_point_sprite = ActorPlacement(
            self.game_map, self).items_point_set()

        self.game_level.floor_sprites = floor_sprite
        self.game_level.wall_sprites = wall_sprite
        self.game_level.map_point_sprites = map_point_sprite
        self.game_level.map_obj_sprites = map_obj_sprite
        self.game_level.actor_sprites = actorsprite
        self.game_level.item_sprites = itemsprite
        self.game_level.item_point_sprites = items_point_sprite
        self.game_level.equip_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.game_level.effect_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.game_level.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.game_level.chara_sprites.append(player)

        self.game_level.level = self.level

        # self.player = Player(
        #     self.game_map.player_position[0], self.game_map.player_position[1], inventory=Inventory(capacity=5))
        # self.game_level.chara_sprites.append(self.player)

        # テスト用エンティティ
        self.long_sword = LongSword(self.player.x, self.player.y + 1)
        self.game_level.item_sprites.append(self.long_sword)
        self.short_sword = ShortSword(self.player.x+1, self.player.y + 1)
        self.game_level.item_sprites.append(self.short_sword)

        self.small_shield = SmallShield(self.player.x + 2, self.player.y+1)
        self.game_level.item_sprites.append(self.small_shield)

        self.cnf = ConfusionScroll(self.player.x + 1, self.player.y)
        self.game_level.item_sprites.append(self.cnf)

        self.fb = FireballScroll(self.player.x + 1, self.player.y)
        self.game_level.item_sprites.append(self.fb)

        self.hp = HealingPotion(self.player.x, self.player.y-1)
        self.game_level.item_sprites.append(self.hp)

        self.boomerang = Boomerang(self.player.x-1, self.player.y + 1)
        self.game_level.item_sprites.append(self.boomerang)

        self.cirsium = Cirsium(self.player.x + 1, self.player.y)
        self.game_level.item_sprites.append(self.cirsium)

        self.fov_recompute = True

        return self.game_level

    def setup(self):

        arcade.set_background_color(COLORS["black"])

        self.cur_level = self.setup_level(level_number=1)
        self.stories.append(self.cur_level)
        self.turn_loop = TurnLoop(self.player)
        self.item_point = ItemPoint(self)

    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}

    def get_dict(self):
        """ オブジェクトをjsonにダンプする為の辞書を作る関数 """

        player_dict = self.get_actor_dict(self.player)

        levels_dict = []
        for level in self.stories:

            actor_dict = []
            for sprite in level.actor_sprites:
                actor_dict.append(self.get_actor_dict(sprite))

            floor_dict = []
            for sprite in level.floor_sprites:
                floor_dict.append(self.get_actor_dict(sprite))

            wall_dict = []
            for sprite in level.wall_sprites:
                wall_dict.append(self.get_actor_dict(sprite))

            map_point_dict = []
            for sprite in level.map_point_sprites:
                map_point_dict.append(self.get_actor_dict(sprite))

            dungeon_obj_dict = []
            for sprite in level.map_obj_sprites:
                dungeon_obj_dict.append(self.get_actor_dict(sprite))

            item_dict = []
            for sprite in level.item_sprites:
                item_dict.append(self.get_actor_dict(sprite))

            item_point_dict = []
            for sprite in level.item_point_sprites:
                item_point_dict.append(self.get_actor_dict(sprite))

            effect_dict = []
            for sprite in level.effect_sprites:
                effect_dict.append(self.get_actor_dict(sprite))

            equip_dict = []
            for sprite in level.equip_sprites:
                equip_dict.append(self.get_actor_dict(sprite))

            level_dict = {
                "actor": actor_dict,
                "floor": floor_dict,
                "wall": wall_dict,
                "map_point": map_point_dict,
                "dungeon_obj": dungeon_obj_dict,
                "item": item_dict,
                "item_point": item_point_dict,
                "effect": effect_dict,
                "equip": equip_dict
            }
            levels_dict.append(level_dict)

        # ビューポートの位置情報を保存
        viewport = arcade.get_viewport()

        result = {"player": player_dict,
                  "viewport": viewport,
                  "levels": levels_dict}

        self.action_queue.append({"message": "*save*"})
        return result

    def restore_from_dict(self, data):
        """ オブジェクトをjsonから復元する為の関数 """

        player_dict = data["player"]
        self.player.restore_from_dict(player_dict["Player"])

        for level_dict in data["levels"]:
            level = GameLevel()

            level.chara_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.actor_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.floor_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.wall_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.map_point_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.map_obj_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.item_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.item_point_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.equip_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.effect_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            for actor_dict in level_dict["actor"]:
                actor = restore_actor(actor_dict)
                level.actor_sprites.append(actor)

            for floor_dict in level_dict["floor"]:
                floors = restore_actor(floor_dict)
                level.floor_sprites.append(floors)

            for wall_dict in level_dict["wall"]:
                walls = restore_actor(wall_dict)
                level.wall_sprites.append(walls)

            for map_point_dict in level_dict["map_point"]:
                map_points = restore_actor(map_point_dict)
                level.map_point_sprites.append(map_points)

            for dungeon_obj_dict in level_dict["dungeon_obj"]:
                map_obj = restore_actor(dungeon_obj_dict)
                level.map_obj_sprites.append(map_obj)

            for item_dict in level_dict["item"]:
                item = restore_actor(item_dict)
                level.item_sprites.append(item)

            for item_point_dict in level_dict["item_point"]:
                item_point = restore_actor(item_point_dict)
                level.item_point_sprites.append(item_point)

            for effect_dict in level_dict["effect"]:
                effect = restore_actor(effect_dict)
                level.effect_sprites.append(effect)

            for equip_dict in level_dict["equip"]:
                equip = restore_actor(equip_dict)
                level.equip_sprites.append(equip)

            level.chara_sprites.append(self.player)

            self.stories.append(level)

        self.cur_level = self.stories[-1]

        # ビューポートを復元する
        arcade.set_viewport(*data["viewport"])

        self.action_queue.append({"message": "*load*"})

    def process_action_queue(self, delta_time):
        """アクターの基本的な行動を制御するアクションキュー
        エンジン内にある各メソッドの返り値(damage, message等)はここに送る
        """
        new_action_queue = []
        for action in self.action_queue:
            if "player_turn" in action:
                print("player_turn")
                self.player.state = state.READY

            if "None" in action:
                pass

            if "message" in action:
                self.messages.append(action["message"])

            if "remove" in action:
                target = action["remove"]
                target.remove_from_sprite_lists()

            if "turn_end" in action:
                target = action["turn_end"]
                target.wait = target.speed
                target.state = state.TURN_END
                print(f"{target.name} is pass Turn_END")

            if "dead" in action:
                print("Death")
                target = action["dead"]
                target.color = COLORS["dead"]
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "player has died!"}])
                else:
                    self.player.fighter.current_xp += target.fighter.xp_reward
                    self.move_switch = False

                    new_action_queue.extend(
                        [{"message": f"{target.name} has been killed!"}])

                    new_action_queue.extend(
                        [{"delay": {"time": DEATH_DELAY, "action": {"remove": target}}}])

            if "delay" in action:
                target = action["delay"]
                target["time"] -= delta_time
                if target["time"] > 0:
                    new_action_queue.extend([{"delay": target}])
                    self.move_switch = False
                else:
                    new_action_queue.extend([target["action"]])
                    self.move_switch = True

            if "select_item" in action:
                item_number = action["select_item"]
                if 1 <= item_number <= self.player.inventory.capacity:
                    if self.selected_item != item_number - 1:
                        self.selected_item = item_number - 1

            if "use_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item and Tag.used in item.tag:
                        results = item.use(self)
                        if results:
                            new_action_queue.extend(results)
                            self.player.state = state.TURN_END

            if "equip_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(
                        item_number)
                    if item and Tag.equip in item.tag:
                        results = self.player.equipment.toggle_equip(
                            item, self.cur_level.equip_sprites)
                        new_action_queue.extend(results)

            if "pickup" in action:
                items = arcade.get_sprites_at_point(
                    (self.player.center_x, self.player.center_y), self.cur_level.item_sprites)
                for item in items:
                    if Tag.item in item.tag:
                        results = self.player.inventory.add_item(item, self)

                        if results:
                            new_action_queue.extend(results)
                            # mapからPOINTを消す
                            if "You pick up" in "".join(list(*results[0].values())):
                                self.item_point.remove_point(item)

            if "drop_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)

                    # これはequipを外す処理
                    if item and item in self.player.equipment.item_slot.values():
                        self.player.equipment.toggle_equip(
                            item, self.cur_level.equip_sprites)

                    # ここでドロップ
                    if item:
                        self.player.inventory.remove_item_number(item_number)
                        item.x = self.player.x
                        item.y = self.player.y
                        self.item_point.add_point(item)  # mapにPOINTを表示
                        self.cur_level.item_sprites.append(item)
                        new_action_queue.extend(
                            [{"message": f"You dropped the {item.name}"}])

            if "use_stairs" in action:
                result = self.use_stairs()
                if result:
                    new_action_queue.extend(result)
                    self.game_state = GAME_STATE.NORMAL
                    self.turn_loop = TurnLoop(self.player)
                    self.fov_recompute = True

            if "grid_select" in action:
                self.game_state = GAME_STATE.SELECT_LOCATION

            if "close_door" in action:
                self.player.state = state.DOOR
                new_action_queue.extend(
                    [{"message": f"What direction do you want the door to close?"}])

            if "use_door" in action:
                door_dist = (action["use_door"])
                result = self.use_door(door_dist)
                if result:
                    new_action_queue.extend(result)

            if "fire" in action:
                shooter = action["fire"]
                fire = Fire(self, shooter=shooter)
                result = fire.shot()
                if result:
                    new_action_queue.extend(result)

            if "damage_pop" in action:
                target = action["damage_pop"]
                damage = action["damage"]
                Damagepop(self, damage, arcade.color.ORANGE_PEEL, target)

            if "talk" in action:
                actor = action.pop("talk")
                if hasattr(actor, "message_event"):
                    self.game_state = GAME_STATE.MESSAGE_WINDOW
                    self.messenger = actor
                else:
                    actor.center_x, actor.center_y = self.player.center_x, self.player.center_y
                    actor.x, actor.y = self.player.x, self.player.y
                action = None

        self.action_queue = new_action_queue

    def grid_click(self, grid_x, grid_y):
        """ クリックしたグリッドをself.grid_select_handlersに格納する 
        """
        for f in self.grid_select_handlers:
            results = f(grid_x, grid_y)
            if results:
                self.action_queue.extend(results)
        self.grid_select_handlers = []

    def fov(self):
        """recompute_fovでTCODによるFOVの計算を行い
           fov_getで表示するスプライトを制御する
        """
        if self.fov_recompute == True:
            recalculate_fov(self.player.x, self.player.y, FOV_RADIUS,
                            [self.cur_level.wall_sprites, self.cur_level.floor_sprites, self.cur_level.actor_sprites, self.cur_level.item_sprites, self.cur_level.map_obj_sprites, self.cur_level.map_point_sprites, self.cur_level.item_point_sprites])

            self.fov_recompute = False

    def check_for_player_movement(self, dist):
        """プレイヤーの移動
        """
        if self.player.state == state.READY and dist and self.move_switch:
            attack = self.player.move(dist, None, self)
            if attack:
                self.action_queue.extend(attack)
                # self.move_switch = False
            dist = None

    def use_stairs(self):
        """階段及びplayerの位置の判定
        """
        get_stairs = arcade.get_sprites_at_exact_point(
            point=self.player.position,
            sprite_list=self.cur_level.map_obj_sprites)

        for stairs in get_stairs:
            if isinstance(stairs, Stairs):
                self.game_state = GAME_STATE.DELAY_WINDOW
                self.player.state = state.DELAY
                player_dict = self.get_actor_dict(self.player)
                level = self.setup_level(self.cur_level.level + 1)
                self.cur_level = level
                self.stories.append(level)
                tx, ty = self.player.x, self.player.y
                tmp_x, tmp_y = self.player.center_x, self.player.center_y
                self.player.restore_from_dict(player_dict["Player"])
                self.player.x = tx
                self.player.y = ty
                self.player.center_x = tmp_x
                self.player.center_y = tmp_y
                self.player.state = state.READY

                return [{"message": "You went down a level."}]
        return [{"message": "There are no stairs here"}]

    def use_door(self, door_dist):
        result = []
        dx, dy = door_dist
        dest_x = self.player.x + dx
        dest_y = self.player.y + dy
        door_actor = get_door(dest_x, dest_y, self.cur_level.map_obj_sprites)
        enemy_actor = get_blocking_entity(
            dest_x, dest_y, [self.cur_level.actor_sprites])
        if door_actor and not enemy_actor:
            door_actor = door_actor[0]
            if door_actor.left_face:
                door_actor.left_face = False
            elif not door_actor.left_face:
                door_actor.left_face = True

            result.extend(
                [{"delay": {"time": 0.2, "action": {"turn_end": self.player}}}])
        elif door_actor and enemy_actor:
            result.extend(
                [{"message": f"We can't close the door because of the {enemy_actor[0].name}."}])
            result.extend(
                [{"delay": {"time": 0.2, "action": {"player_turn"}}}])
        else:
            result.extend([{"message": f"There is no door in that direction"}])
            result.extend(
                [{"delay": {"time": 0.2, "action": {"player_turn"}}}])

        return result
