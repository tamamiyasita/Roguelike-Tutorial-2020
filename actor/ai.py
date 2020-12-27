from os import remove
import arcade
from random import randint, choice
from astar import astar
from constants import *
from util import stop_watch



class Wait:
    def __init__(self):
        self.owner = None
        self.visible_check = None

    def take_turn(self, engine=None):
        results = []

        dice = randint(1,6)
        if len(self.owner.fighter.skill_list) >= 1 and dice < 2:
            use_skill = {"use_skill": 1, "user":self.owner}
            results.append(use_skill)
            return results
        message = choice(self.owner.message)
        results.append(message)
        results.extend([{"turn_end": self.owner}])

        return results


class RandomMove:
    def __init__(self):
        self.owner = None
        self.visible_check = None

    def take_turn(self, engine=None):
        results = []
        dice = randint(1,6)
        if dice <= 5: 
            self.owner.move((randint(-1, 1), randint(-1, 1)), engine=engine)

        message = choice(self.owner.message)
        results.append(message)

        return results


class Basicmonster:
    def __init__(self, target_point=None, visible_check=False):
        self.owner = None
        self.target_point = target_point  # targetの位置を格納する
        self.visible_check = visible_check  # 視野に入った場合チェックされ,Trueなら移動する

    @stop_watch
    def take_turn(self, target, engine):
        results = []
        monster = self.owner

        # sprite_listsのactor_spritesとmap_spritesを変数に格納
        actor_sprites = engine.cur_level.actor_sprites
        wall_sprites = engine.cur_level.wall_sprites

        # 視野のチェック
        if monster.is_visible:
            self.visible_check = True

        # ターゲット座標の更新
        if target:
            self.target_point = target.x, target.y

        # ターゲット座標と自分の座標が同じなら視野とターゲットの変数をクリア
        if (monster.x, monster.y) == self.target_point:
            self.target_point = None
            self.visible_check = False

        # ターゲットに隣接している場合パスは計算しない
        if target and monster.distance_to(target) <= 1.46 and self.visible_check:
            attack = monster.move_towards(target, engine)
            if attack:
                results.extend(attack)
                return results

        if self.visible_check:
            if monster.distance_to(target) >= 1:
                result_astar = astar(
                    [actor_sprites, wall_sprites], (monster.x, monster.y), (self.target_point))
                # print(f"Path from ({monster.x},{monster.y}) to {target.x},{target.y}", results)
                # monster.move_towards(target.x, target.y, sprite_lists)
                # monster.move((randint(-1, 1), randint(-1, 1)))

                # results[1]がターゲットパスへの最初のタイル座標なので変数pointに格納
                if result_astar:
                    point = result_astar[1]
                    x, y = point
                    # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                    dx = x - monster.x
                    dy = y - monster.y

                    attack = monster.move(
                        (dx, dy), target, engine)
                    if attack:
                        results.extend(attack)

                elif not result_astar:
                    result_astar = astar(
                        [wall_sprites], (monster.x, monster.y), (self.target_point))
                    if result_astar:
                        point = result_astar[1]
                        x, y = point
                        # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                        dx = x - monster.x
                        dy = y - monster.y

                        attack = monster.move(
                            (dx, dy), target, engine)
                        if attack:
                            results.extend(attack)

                    elif not result_astar:
                        results.extend([{"turn_end": monster}])

            return results

        else:
            results.extend([{"pass": monster}])
            return results


class ConfusedMonster:
    def __init__(self, pre_ai=None, confused_turn=50):
        self.owner = None
        self.pre_ai = pre_ai
        self.visible_check = None
        self.confused_turn = confused_turn

    def get_dict(self):
        result = {}
        result["pre_ai"] = self.pre_ai.__class__.__name__
        result["confused_turn"] = self.confused_turn
        return result

    def restore_from_dict(self, result):
        if result["pre_ai"] == "Basicmonster":
            self.pre_ai = Basicmonster()
        self.confused_turn = result["confused_turn"]

    def take_turn(self, target, engine):
        results = []
        monster = self.owner

        if self.confused_turn > 0:
            attack = monster.move(
                (randint(-1, 1), randint(-1, 1)), None, engine)
            if attack:
                results.extend(attack)

            self.confused_turn -= 1
            print(f"confused_turn: {self.confused_turn}")

        else:
            # self.ownerにselfを渡し忘れるとロードした時元のAIにselfが渡されず無限ループするので注意
            monster.ai = self.pre_ai
            monster.ai.owner = monster  # self.owner.ai.owner = self.ownerというややこしい表現になる
            results.append(
                {"message": f"The {monster.name} is no longer confused"})
            results.extend([{"pass": monster}])

        return results
