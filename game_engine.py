
import arcade
from collections import deque

from constants import *
from data import *
from game_map.basic_dungeon import BasicDungeon
from game_map.map_sprite_set import ActorPlacement
from recalculate_fov import recalculate_fov
from viewport import viewport

from actor.inventory import Inventory
from actor.confusion_scroll import ConfusionScroll
from actor.PC import Player
from actor.Crab import Crab
from actor.stairs import Stairs
from actor.restore_actor import restore_actor
from actor.short_sword import ShortSword
from actor.small_shield import SmallShield


class GameLevel:
    """現マップのレベルを設定する
    """
    def __init__(self):
        self.chara_sprites = None
        self.actor_sprites = None
        self.map_sprites = None
        self.item_sprites = None
        self.effect_sprites = None
        self.level = 0
        


class GameEngine:
    def __init__(self):
        """ 変数の初期化 """
        self.levels = []
        self.cur_level_index = 0
        self.cur_level = None

        self.player = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=4)
        self.selected_item = None
        self.turn_check = []
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []

        # self.chara_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=32)
        # self.actor_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=32)
        # self.map_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=32)
        # self.item_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=32)        
        # self.effect_sprites = arcade.SpriteList(
        #     use_spatial_hash=True, spatial_hash_cell_size=16)

    def setup(self):

        arcade.set_background_color(arcade.color.BLACK)

        self.cur_level = self.setup_level(1)
        self.levels.append(self.cur_level)

    def setup_level(self, level_number):

        map_width, map_height = MAP_WIDTH, MAP_HEIGHT
        level = GameLevel()

        self.game_map = BasicDungeon(map_width, map_height, level)

        """ スプライトリストの初期化 """
        mapsprite = ActorPlacement(self.game_map, self).map_set()
        actorsprite = ActorPlacement(self.game_map, self).actor_set()
        itemsprite = ActorPlacement(self.game_map, self).items_set()

        level.map_sprites = mapsprite
        level.actor_sprites = actorsprite
        level.item_sprites = itemsprite
        level.effect_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=16)
        level.chara_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)

        level.level = level_number

        self.player = Player(self.game_map.player_position[0],self.game_map.player_position[1], inventory=Inventory(capacity=4))
        level.chara_sprites.append(self.player)

        self.short_sword = ShortSword(self.player.x, self.player.y +1)
        level.item_sprites.append(self.short_sword)

        self.small_shield = SmallShield(self.player.x + 1 , self.player.y+1)
        level.item_sprites.append(self.small_shield)

        self.cnf = ConfusionScroll(self.player.x + 1, self.player.y)
        level.item_sprites.append(self.cnf)

        self.fov_recompute = True

        return level

        




    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}

    def get_dict(self):
        """ オブジェクトをjsonにダンプする為の辞書を作る関数 """

        player_dict = self.get_actor_dict(self.player)

        levels_dict = []
        for level in self.levels:


            actor_dict = []
            for sprite in level.actor_sprites:
                actor_dict.append(self.get_actor_dict(sprite))

            dungeon_dict = []
            for sprite in level.map_sprites:
                dungeon_dict.append(self.get_actor_dict(sprite))

            item_dict = []
            for sprite in level.item_sprites:
                item_dict.append(self.get_actor_dict(sprite))

            effect_dict = []
            for sprite in level.effect_sprites:
                effect_dict.append(self.get_actor_dict(sprite))


            level_dict = {
                         "actor": actor_dict,
                         "dungeon": dungeon_dict,
                         "item": item_dict,
                         "effect": effect_dict,
                         }
            levels_dict.append(level_dict)

        # ビューポートの位置情報を保存
        viewport = arcade.get_viewport()

        result = {"player":player_dict,
                  "viewport": viewport,
                  "levels": levels_dict}

        self.action_queue.append({"message":"*save*"})
        return result

    def restore_from_dict(self, data):
        """ オブジェクトをjsonから復元する為の関数 """

        # ビューポートを復元する
        arcade.set_viewport(*data["viewport"])


        player_dict = data["player"]
        self.player.restore_from_dict(player_dict["Player"])


        for level_dict in data["levels"]:
            level = GameLevel()

            level.chara_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.actor_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.map_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=32)

            level.item_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)

            level.effect_sprites = arcade.SpriteList(
                use_spatial_hash=True, spatial_hash_cell_size=16)



            for actor_dict in level_dict["actor"]:
                actor = restore_actor(actor_dict)
                level.actor_sprites.append(actor)

            for dungeon_dict in level_dict["dungeon"]:
                maps = restore_actor(dungeon_dict)
                level.map_sprites.append(maps)

            for item_dict in level_dict["item"]:
                item = restore_actor(item_dict)
                level.item_sprites.append(item)

            for effect_dict in level_dict["effect"]:
                effect = restore_actor(effect_dict)
                level.effect_sprites.append(effect)

            level.chara_sprites.append(self.player)

            self.levels.append(level)
        
        self.cur_level = self.levels[-1]

        self.action_queue.append({"message":"*load*"})

    def process_action_queue(self, delta_time):
        """アクターの基本的な行動を制御するアクションキュー
        　　エンジン内にある各メソッドの返り値(damage, message等)はここに送る
        """
        new_action_queue = []
        for action in self.action_queue:
            if "player_turn" in action:
                print("player_turn")
                self.player.state = state.READY

            if "enemy_turn" in action:
                print("enemy_turn")
                # self.turn_checkにターン終了フラグを入れる
                self.turn_check = self.move_enemies(self.player)

            if "message" in action:
                self.messages.append(action["message"])

            if "dead" in action:
                print("Death")
                target = action["dead"]
                target.color = arcade.color.GRAY_BLUE
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "player has died!"}])
                else:
                    self.player.fighter.current_xp += target.fighter.xp_reward
                    
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
                    (self.player.center_x, self.player.center_y), self.cur_level.item_sprites)
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

            if "equip_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    equip_item = self.player.inventory.get_item_number(item_number)
                    if equip_item and equip_item.equippable:
                        equip_results = self.player.equipment.toggle_equip(equip_item)

                        for equip in equip_results:
                            equipped = equip.get("equipped")
                            dequipped = equip.get("dequipped")
                     

                            if equipped:
                                new_action_queue.extend([{"message":f"You equipped the {equipped.name}"}])
                                if equipped.equippable.slot.name == "MAIN_HAND":
                                    self.player.inventory.on_equip_name["main_hand"] = equipped.name
                                    print(self.player.inventory.on_equip_name)
                                    
                                elif equipped.equippable.slot.name == "OFF_HAND":
                                    self.player.inventory.on_equip_name["off_hand"] = equipped.name
                                    print(self.player.inventory.on_equip_name)

                            elif dequipped:
                                new_action_queue.extend([{"message":f"You dequipped the {dequipped.name}"}])
                            break


            if "drop_item" in action:
                item_number = self.selected_item
                if item_number is not None:
                    item = self.player.inventory.get_item_number(item_number)
                    if item:
                        self.player.inventory.remove_item_number(item_number)
                        self.cur_level.item_sprites.append(item)
                        item.center_x = self.player.center_x
                        item.center_y = self.player.center_y
                        new_action_queue.extend([{"message": f"You dropped the {item.name}"}])

                        if self.player.equipment.main_hand == item or self.player.equipment.off_hand == item:
                            dequipped = self.player.equipment.toggle_equip(item)
                            new_action_queue.extend(dequipped)

            if "use_stairs" in action:

                result = self.use_stairs()
                if result:
                    new_action_queue.extend(result)
                    self.game_state = GAME_STATE.NORMAL

        self.action_queue = new_action_queue

    def grid_click(self, grid_x, grid_y):
        """ クリックしたグリッドをself.grid_select_handlersに格納する 
        """
        for f in self.grid_select_handlers:
            results = f(grid_x, grid_y)
            if results:
                self.action_queue.extend(results)
        self.grid_select_handlers = []

    def move_enemies(self, target):
        """ enemyの行動ターンを制御する
            行動するenemyがいない場合"next_turn"を返す
        """
        actor_check = []
        results = []
        for actor in self.cur_level.actor_sprites:
            if actor.ai and not actor.is_dead:
                results = actor.ai.take_turn(
                    target=target, sprite_lists=[self.cur_level.actor_sprites, self.cur_level.map_sprites])
                if results:
                    self.action_queue.extend(results)
                    actor_check.append(actor)
                # else:
                #     actor.move_towards(
                #         target, self.actor_sprites, self.game_map)
                #     actor_check.append(actor)

                # else:
                #     results = actor.ai.take_turn(
                #         target=target, game_map=self.game_map, sprite_lists=[self.map_sprites])
                #     if results:
                #         self.action_queue.extend(results)
        if not actor_check:
            actor_check.append("next_turn")

        # print(actor_check, "actor_check")
        return actor_check

    def fov(self):
        """recompute_fovでTCODによるFOVの計算を行い
           fov_getで表示するスプライトを制御する
        """
        if self.fov_recompute == True:
            recalculate_fov(self.player.x, self.player.y, FOV_RADIUS,
                            [self.cur_level.map_sprites, self.cur_level.actor_sprites, self.cur_level.item_sprites])

            self.fov_recompute = False

    def check_for_player_movement(self, dist):
        """プレイヤーの移動
        """
        if self.player.state == state.READY and dist:
            attack = self.player.move(dist, None, self.cur_level.actor_sprites, self.cur_level.map_sprites)
            if attack:
                self.action_queue.extend(attack)

    def turn_change(self, delta_time):
        """ playerとenemyの行動ターンを切り替える
        """

        # playerがTURN_END状態になるとキューに"enemy_turn"を送信する
        if self.player.state == state.TURN_END:
            self.fov_recompute = True
            self.player.state = state.DELAY
            self.action_queue.extend([{"enemy_turn": True}])

        # move_enemies関数が"next_turn"を返した場合キューに"player_turn"を送信する
        elif "next_turn" in self.turn_check:
            self.turn_check = []
            self.action_queue.extend([{"player_turn": True}])

        # 全てのenemyがTURN_END状態になった場合キューに"player_turn"を返す
        elif self.turn_check:
            # enemyのTURN_ENDをカウントする変数
            # TODO setを使って効率化したい
            turn_count = 0
            for actor in self.turn_check:
                if actor.state == state.TURN_END:
                    turn_count += 1
                # print(len(self.turn_check), turn_count, "Trun check count")
                if turn_count >= len(self.turn_check):
                    self.action_queue.extend([{"player_turn": True}])
                    self.turn_check = []

    def use_stairs(self):
        """階段及びplayerの位置の判定
        """
        get_stairs = arcade.get_sprites_at_exact_point(self.player.position, self.cur_level.map_sprites)

        for stairs in get_stairs:
            if isinstance(stairs, Stairs):
                self.game_state = GAME_STATE.DELAY_WINDOW
                self.player.state = state.DELAY
                player_dict = self.get_actor_dict(self.player)
                level = self.setup_level(self.cur_level.level + 1)
                self.cur_level = level
                self.levels.append(level)
                tx, ty = self.player.x, self.player.y
                tmp_x, tmp_y = self.player.center_x, self.player.center_y
                self.player.restore_from_dict(player_dict["Player"])
                self.player.x = tx
                self.player.y = ty
                self.player.center_x = tmp_x
                self.player.center_y = tmp_y
                self.player.state = state.READY
                viewport(self.player)



                return [{"message": "You went down a level."}]
        return [{"message": "There are no stairs here"}]
