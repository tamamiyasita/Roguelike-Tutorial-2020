import arcade
from random import randint
from astar import astar
from constants import *


class Basicmonster:
    def __init__(self):
        self.owner = None
        self.target_point = None # targetの位置を格納する
        self.visible_check = False # 視野に入った場合チェックされ,Trueなら移動する

    def take_turn(self, target, sprite_lists):
        results = []
        monster = self.owner

        # sprite_listsのactor_spritesとmap_spritesを変数に格納
        actor_sprites = sprite_lists[0]
        map_sprites = sprite_lists[1]


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
            attack = monster.move_towards(target, actor_sprites, map_sprites)
            if attack:
                results.extend(attack)
                print("move_towards attack")
                return results


        if self.visible_check:
            if monster.distance_to(target) >= 1:
                results = astar(
                    sprite_lists, (monster.x, monster.y), (self.target_point))
                # print(f"Path from ({monster.x},{monster.y}) to {target.x},{target.y}", results)
                # monster.move_towards(target.x, target.y, sprite_lists)
                # monster.move((randint(-1, 1), randint(-1, 1)))

                # results[1]がターゲットパスへの最初のタイル座標なので変数pointに格納
                if results:
                    point = results[1]
                    x, y = point
                    # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                    dx = x - monster.x
                    dy = y - monster.y

                    attack = monster.move(
                        (dx, dy), target, actor_sprites, map_sprites)
                    if attack:
                        results.extend(attack)
            return results

        else:
            results.append({"pass": monster})
            return results


class ConfusedMonster:
    def __init__(self, pre_ai, confused_turn=10):
        self.pre_ai = pre_ai
        self.confused_turn = confused_turn

    def take_turn(self, target, sprite_lists):
        results = []
        monster = self.owner
        actor_sprites = sprite_lists[0]
        map_sprites = sprite_lists[1]

        if self.confused_turn > 0:
            attack = monster.move(
                (randint(-1, 1), randint(-1, 1)), None, actor_sprites, map_sprites)
            if attack:
                results.extend(attack)

            self.confused_turn -= 1

        else:
            monster.ai = self.pre_ai
            results.append(
                {"message": f"The {monster.name} is no longer confused"})

        return results
