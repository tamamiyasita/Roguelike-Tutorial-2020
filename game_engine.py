
import arcade
from collections import deque

from constants import *
from data import *
from game_map.basic_dungeon import BasicDungeon
from game_map.town_map import TownMap
from game_map.map_sprite_set import ActorPlacement
from game_map.test_map import TestMap

from recalculate_fov import recalculate_fov

from actor.inventory import Inventory
from actor.item_point_check import ItemPoint
from actor.characters.PC import Player
from actor.characters.orcs import Orc
from actor.characters.rat import Water_vole
from actor.characters.npc import Citizen
from actor._actor import Actor

from actor.map_obj.stairs import Up_Stairs, Down_Stairs
from actor.restore_actor import restore_actor
from util import get_door, get_blocking_entity, stop_watch
from turn_loop import TurnLoop
from fire import Fire
from actor.items.boomerang import Boomerang
from actor.damage_pop import Damagepop

from actor.items.short_sword import ShortSword
from actor.items.long_sword import LongSword
from actor.items.confusion_scroll import ConfusionScroll
from actor.items.fireball_scroll import FireballScroll
from actor.items.small_shield import SmallShield
from actor.items.paeonia import Paeonia
from actor.items.cirsium import Cirsium
from actor.items.ebony import Ebony
from actor.items.sunflower import Sunflower
from level_up_sys import check_experience_level



class GameLevel:
    """dungeon階層毎にsprite_listを生成し、self.storiesに格納する"""

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

        self.map_name = None
        self.floor_level = None

class GameEngine:
    def __init__(self):
        self.stories = {}  # 階層を格納する変数
        self.cur_level = None

        self.player = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=9)
        self.selected_item = 0  # キー押下で直接選択したアイテム
        self.turn_check = []
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []
        self.move_switch = True
        self.damage_pop = []
        self.messenger = None

        self.player = Player(
            inventory=Inventory(capacity=9))



    def setup_level(self, level_number):
        """未踏の階層を生成する"""

        self.map_width, self.map_height = MAP_WIDTH, MAP_HEIGHT
        self.game_level = GameLevel()

        if level_number == 0:
            return self.start_town_init()
        elif level_number >= 99:
            return self.test_map(level_number)
        elif level_number >= 1:
            cur_map = self.basic_dungeon_init(level_number)
            return cur_map

    def setup(self):

        arcade.set_background_color(COLORS["black"])
        self.flower_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        self.tmp_effect_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        self.cur_level = self.setup_level(level_number=99)
        self.stories[self.cur_floor_name] = self.cur_level
        self.turn_loop = TurnLoop(self.player)
        self.item_point = ItemPoint(self)

    def test_map(self, level):
        self.game_map = TestMap(40,40,99)
        #スプライトリストの初期化
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
        self.game_level.chara_sprites.append(self.player)

        self.player.x, self.player.y = 10, 10

        self.wb = Water_vole(x=10,y=17)
        self.game_level.actor_sprites.append(self.wb)
        self.wb2 = Water_vole(x=11,y=17)
        self.game_level.actor_sprites.append(self.wb2)

        self.npc = Citizen(x=14,y=14)
        self.game_level.actor_sprites.append(self.npc)

        self.game_level.floor_level = level
        self.game_level.map_name = f"test_dungeon"

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

        self.hp = Paeonia(self.player.x-1, self.player.y)
        self.game_level.item_sprites.append(self.hp)

        self.boomerang = Boomerang(self.player.x-1, self.player.y + 1)
        self.game_level.item_sprites.append(self.boomerang)

        self.cirsium = Cirsium(self.player.x + 1, self.player.y)
        self.game_level.item_sprites.append(self.cirsium)

        self.ebony = Ebony(self.player.x + 1, self.player.y-1)
        self.game_level.item_sprites.append(self.ebony)

        self.sunflower = Sunflower(self.player.x, self.player.y-2)
        self.game_level.item_sprites.append(self.sunflower)


        self.st = Up_Stairs(self.player.x + 1, self.player.y-1)
        self.st.scale = 2
        self.game_level.map_obj_sprites.append(self.st)

        self.ut = Down_Stairs(self.player.x, self.player.y-1)
        self.ut.scale = 2
        self.game_level.map_obj_sprites.append(self.ut)

        return self.game_level

    def start_town_init(self):
        """初期townmapの生成"""
        self.town_map = TownMap(
            self.map_width, self.map_height)
        self.town_map.player_set(self.player)
        # スプライトリストの初期化
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

        self.game_level.floor_level = 0

        self.game_level.map_name = f"town"

        return self.game_level

    def basic_dungeon_init(self, level=1, stairs=None):
        """基本のdungeonの生成"""
        self.game_map = BasicDungeon(
            self.map_width, self.map_height, level)

        #スプライトリストの初期化
        wall_sprite = ActorPlacement(self.game_map, self).wall_set()
        floor_sprite = ActorPlacement(self.game_map, self).floor_set()
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
        self.game_level.chara_sprites.append(self.player)

        self.player.x, self.player.y = self.game_map.player_set(stairs)

        self.game_level.floor_level = level
        self.game_level.map_name = f"basic_dungeon"



        self.ut = Down_Stairs(self.player.x, self.player.y-1)
        self.ut.scale = 2
        self.game_level.map_obj_sprites.append(self.ut)

        self.fov_recompute = True

        return self.game_level


    @property
    def cur_floor_name(self):
        return f"{self.cur_level.map_name}{self.cur_level.floor_level}"


    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}
    @stop_watch
    def get_dict(self):
        """ オブジェクトをjsonにダンプする為の辞書を作る関数 """
        self.game_state = GAME_STATE.DELAY_WINDOW
        ##############


        player_dict = self.get_actor_dict(self.player)

        levels_dict = {}
        for map_name, level in self.stories.items():


            actor_dict = [self.get_actor_dict(s) for s in level.actor_sprites]
            floor_dict = [self.get_actor_dict(s) for s in level.floor_sprites]
            wall_dict = [self.get_actor_dict(s) for s in level.wall_sprites]
            map_point_dict = [self.get_actor_dict(s) for s in level.map_point_sprites]
            dungeon_obj_dict = [self.get_actor_dict(s) for s in level.map_obj_sprites]
            item_dict = [self.get_actor_dict(s) for s in level.item_sprites]
            item_point_dict = [self.get_actor_dict(s) for s in level.item_point_sprites]
            effect_dict = [self.get_actor_dict(s) for s in level.effect_sprites]


            level_dict = {
                "level":level.floor_level,
                "map_name":level.map_name,

                "actor": actor_dict,
                "floor": floor_dict,
                "wall": wall_dict,
                "map_point": map_point_dict,
                "dungeon_obj": dungeon_obj_dict,
                "item": item_dict,
                "item_point": item_point_dict,
                "effect": effect_dict,
            }
            levels_dict[map_name] = level_dict

        # ビューポートの位置情報を保存
        viewport = arcade.get_viewport()

        result = {"player": player_dict,
                  "viewport": viewport,
                  "levels": levels_dict,
                  "cur_level_name":f"{self.cur_level.map_name}{self.cur_level.floor_level}",
                  }

        ##############
        self.action_queue.append({"message": "*save*"})
        self.game_state = GAME_STATE.NORMAL
        print(f"**save**{result=}")
        return result

    def restore_from_dict(self, data):
        """ オブジェクトをjsonから復元する為の関数 """
        self.game_state = GAME_STATE.DELAY_WINDOW
        self.player.state = state.DELAY

        print("**load**")
        ####################

        player_dict = data["player"]
        self.player.restore_from_dict(player_dict["Player"])

        self.town_map = TownMap(self.map_width, self.map_height)

        for map_name, level_dict in data["levels"].items():
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
            

            level.floor_level = level_dict["level"]
            level.map_name = level_dict["map_name"]

            level.chara_sprites.append(self.player)

            for actor_dict in level_dict["actor"]:
                actor = restore_actor(actor_dict)
                level.actor_sprites.append(actor)

            if map_name == "town0":
                floors = ActorPlacement(self.town_map, self).tiled_floor_set()
                for f in floors:
                    level.floor_sprites.append(f)

            else:
                for floor_dict in level_dict["floor"]:
                    floors = restore_actor(floor_dict)
                    level.floor_sprites.append(floors)

            if map_name == "town0":
                walls = ActorPlacement(self.town_map, self).tiled_wall_set()
                for w in walls:
                    level.wall_sprites.append(w)
            else:
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



            self.stories[map_name] = level
        print(self.stories)
        self.flower_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
        self.tmp_effect_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)

        self.cur_level = self.stories[data["cur_level_name"]]#dataに格納した現在階層を適応する 


        # ビューポートを復元する
        arcade.set_viewport(*data["viewport"])

        
        ####################
        self.action_queue.append({"message": "*load*"})
        self.player.state = state.READY
        self.game_state = GAME_STATE.NORMAL
        self.fov_recompute = True
        self.player.equipment.item_sprite_check(self.flower_sprites)
        self.player.equipment.equip_position_reset()


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
                # ここでplayerにEXPが入る
                check_experience_level(self.player, self)

            if "turn_end" in action:
                target = action["turn_end"]
                target.wait = target.speed
                target.state = state.TURN_END
                print(f"{target.name} is pass Turn_END")

            if "dead" in action:
                target = action["dead"]
                target.color = COLORS["dead"]
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "player has died!"}])
                else:
                    # EXP獲得処理
                    self.player.fighter.current_xp += target.fighter.xp_reward
                    self.player.equipment.item_exp_add(target.fighter.xp_reward)
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

            if "fire" in action:
                shooter = action["fire"]
                fire = Fire(self, shooter=shooter)
                result = fire.shot()
                if result:
                    new_action_queue.extend(result)
    
            if "use_skill" in action:
                select_skill = action["use_skill"]
                user = action["user"]
                if select_skill and user:
                    skill = user.fighter.active_skill
    
                    if select_skill is not None and len(skill) >= select_skill:
                        skill = skill[select_skill-1]
                        if skill and Tag.active in skill.tag:
                            results = skill.use(self)
                            if results:
                                new_action_queue.extend(results)



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
                        results = self.player.equipment.toggle_equip(item)
                        if results:
                            if "dequipped" in results[0]["message"]:
                                self.flower_sprites.remove(item)
                            else:
                                self.flower_sprites.append(item)
                            
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
                    if item and item in self.player.equipment.item_slot:
                        self.player.equipment.toggle_equip(item)

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
                    self.flower_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)
                    self.tmp_effect_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)

                    self.player.equipment.passive_sprite_on(self.flower_sprites)
                    self.player.equipment.item_sprite_check(self.flower_sprites)
                    self.player.equipment.equip_position_reset()
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


            if "damage_pop" in action:
                target = action["damage_pop"]
                damage = action["damage"]
                txt_color =arcade.color.WHITE
                if 0 < damage:
                    txt_color = arcade.color.MINT_GREEN
                elif 0 > damage:
                    txt_color = COLORS["status_bar_foreground"]

                Damagepop(self, damage, txt_color, target)

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

        player_dict = self.get_actor_dict(self.player)
        


        for stairs in get_stairs:
            if isinstance(stairs, Down_Stairs):
                cur_level_name = f"{self.cur_level.map_name}{self.cur_level.floor_level}"

                next_level = self.setup_level(self.cur_level.floor_level + 1)
                next_level_name = f"{next_level.map_name}{self.cur_level.floor_level+1}"

                self.stories[cur_level_name] = self.cur_level
                if next_level_name not in self.stories.keys():
                    self.cur_level = next_level
        
                    up_stairs = [i for i in self.cur_level.map_obj_sprites if isinstance(i, Up_Stairs)]
                    self.player.restore_from_dict(player_dict["Player"])
                    self.stories[next_level_name] = self.cur_level
                    self.player.x, self.player.y = up_stairs[0].x, up_stairs[0].y


                else:
                    load_level = self.stories[next_level_name]
                    self.cur_level = load_level
                    self.cur_level.floor_level = load_level.floor_level
                
                    up_stairs = [i for i in self.cur_level.map_obj_sprites if isinstance(i, Up_Stairs)]
                    self.player.restore_from_dict(player_dict["Player"])
                    self.player.x, self.player.y = up_stairs[0].x, up_stairs[0].y


                self.player.state = state.READY
                return [{"message": "You went down a level."}]

        for stairs in get_stairs:
            if isinstance(stairs, Up_Stairs):
                prev_level_name = f"{self.cur_level.map_name}{self.cur_level.floor_level-1}"
                self.stories[f"{self.cur_level.map_name}{self.cur_level.floor_level}"] = self.cur_level
                return_level = (self.cur_level.floor_level - 1)

                if 0 == return_level:

                    load_level = self.stories[f"town0"]
                    self.cur_level = load_level

                    down_stairs = [i for i in self.cur_level.map_obj_sprites if isinstance(i, Down_Stairs)]
                    self.player.restore_from_dict(player_dict["Player"])
                    self.player.x, self.player.y = down_stairs[0].x, down_stairs[0].y

                elif -1 >= return_level:
                    raise ValueError

                else:
                    self.cur_level = self.stories[prev_level_name]

                    down_stairs = [i for i in self.cur_level.map_obj_sprites if isinstance(i, Down_Stairs)]
                    self.player.restore_from_dict(player_dict["Player"])
                    self.player.x, self.player.y = down_stairs[0].x, down_stairs[0].y
                    
                return [{"message": "You went UP a level."}]

        return None #[{"message": "There are no stairs here"}]




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
