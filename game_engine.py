
import arcade
from collections import deque


from constants import *
from data import *
from game_map.basic_dungeon import BasicDungeon
from game_map.map_sprite_set import ActorPlacement
from recalculate_fov import recalculate_fov

from actor.inventory import Inventory
from actor.confusion_scroll import ConfusionScroll
from actor.PC import Player
from actor.Crab import Crab
from actor.stairs import Stairs
from actor.restore_actor import restore_actor


class GameEngine:
    def __init__(self):
        """ 変数の初期化 """
        self.chara_sprites = None
        self.actor_sprites = None
        self.map_sprites = None
        self.item_sprites = None
        self.player = None
        self.game_map = None
        self.action_queue = []
        self.messages = deque(maxlen=4)
        self.selected_item = None
        self.turn_check = []
        self.game_state = GAME_STATE.NORMAL
        self.grid_select_handlers = []

    def setup(self):
        """ スプライトリストの初期化等 """
        self.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)
        self.effect_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16)

        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)
        mapsprite = ActorPlacement(self.game_map, self).map_set()
        actorsprite = ActorPlacement(self.game_map, self).actor_set()
        itemsprite = ActorPlacement(self.game_map, self).items_set()
        self.map_sprites = mapsprite
        self.actor_sprites = actorsprite
        self.item_sprites = itemsprite


        self.player = Player(
            self.game_map.player_pos[0], self.game_map.player_pos[1], inventory=Inventory(capacity=5))
        self.chara_sprites.append(self.player)
        # self.crab = Crab(self.player.x + 2, self.player.y +
        #                  1, game_engine=self,)
        # self.actor_sprites.append(self.crab)
        self.cnf = ConfusionScroll(
            self.player.x + 1, self.player.y)
        self.item_sprites.append(self.cnf)

        # self.fov_map = initialize_fov(self.game_map)

        self.fov_recompute = True

        arcade.set_background_color(arcade.color.BLACK)

    def get_actor_dict(self, actor):
        name = actor.__class__.__name__
        return {name: actor.get_dict()}

    def get_dict(self):
        """ オブジェクトをjsonにダンプする為の辞書を作る関数 """

        player_dict = self.get_actor_dict(self.player)

        actor_dict = []
        for sprite in self.actor_sprites:
            actor_dict.append(self.get_actor_dict(sprite))

        item_dict = []
        for sprite in self.item_sprites:
            item_dict.append(self.get_actor_dict(sprite))

        dungeon_dict = []
        for sprite in self.map_sprites:
            dungeon_dict.append(self.get_actor_dict(sprite))

        result = {"player": player_dict,
                  "actor": actor_dict,
                  "item": item_dict,
                  "dungeon": dungeon_dict}
        return result

    def restore_from_dict(self, data):
        """ オブジェクトをjsonから復元する為の関数 """

        self.chara_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.actor_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16)

        self.map_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=32)

        self.item_sprites = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=16)

        player_dict = data["player"]
        self.player.restore_from_dict(player_dict["Player"])
        self.chara_sprites.append(self.player)

        # for actor_dict in data["actor"]:
        #     self.crab.restore_from_dict(actor_dict["Crab"])
        #     self.actor_sprites.append(self.crab)

        for actor_dict in data["actor"]:
            actor = restore_actor(actor_dict)
            self.actor_sprites.append(actor)

        for item_dict in data["item"]:
            item = restore_actor(item_dict)
            self.item_sprites.append(item)

        for dungeon_dict in data["dungeon"]:
            maps = restore_actor(dungeon_dict)
            self.map_sprites.append(maps)

    def process_action_queue(self, delta_time):
        """アクターの基本的な行動を制御するアクションキュー
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

            if "use_stairs" in action:
                result = self.use_stairs()
                if result:
                    new_action_queue.extend(result)

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
        turn_check = []
        results = []
        for actor in self.actor_sprites:
            if actor.ai and not actor.is_dead:
                results = actor.ai.take_turn(
                    target=target, sprite_lists=[self.actor_sprites, self.map_sprites])
                if results:
                    self.action_queue.extend(results)
                    turn_check.append(actor)
                # else:
                #     actor.move_towards(
                #         target, self.actor_sprites, self.game_map)
                #     turn_check.append(actor)

                # else:
                #     results = actor.ai.take_turn(
                #         target=target, game_map=self.game_map, sprite_lists=[self.map_sprites])
                #     if results:
                #         self.action_queue.extend(results)
        if not turn_check:
            turn_check.append("next_turn")

        # print(turn_check, "turn_check")
        return turn_check

    def fov(self):
        """recompute_fovでTCODによるFOVの計算を行い
           fov_getで表示するスプライトを制御する
        """
        if self.fov_recompute == True:
            recalculate_fov(self.player.x, self.player.y, FOV_RADIUS,
                            [self.map_sprites, self.actor_sprites, self.item_sprites])

            self.fov_recompute = False

    def check_for_player_movement(self, dist):
        """プレイヤーの移動
        """
        if self.player.state == state.READY and dist:
            attack = self.player.move(dist, None, self.actor_sprites, self.map_sprites)
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
                if turn_count == len(self.turn_check):
                    self.action_queue.extend([{"player_turn": True}])
                    self.turn_check = []

    def use_stairs(self):
        """階段及びplayerの位置の判定
        """
        get_stairs = arcade.get_sprites_at_exact_point(self.player.position, self.map_sprites)

        for stairs in get_stairs:
            if isinstance(stairs, Stairs):
                return [{"message": "You haven't learned how to take the stairs yet."}]
        return [{"message": "There are no stairs here"}]
