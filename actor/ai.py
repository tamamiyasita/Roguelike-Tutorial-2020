
from random import randint, choice
from astar import astar
from constants import *
from util import stop_watch
from game_map.square_grid import breadth_first_search, a_star_search


class Wait:
    def __init__(self):
        self.owner = None
        self.visible_check = None

    def take_turn(self, engine=None):
        results = []
        
        # Skill使用テスト
        # dice = randint(1,6)
        # if len(self.owner.fighter.skill_list) >= 1 and dice < 2:
        #     use_skill = {"use_skill": 1, "user":self.owner}
        #     results.append(use_skill)
        #     return results
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
            results.extend([{"action":(self.owner,(randint(-1, 1), randint(-1, 1)))}])


        message = choice(self.owner.message)
        results.append(message)

        return results


class Rangid_AI:
    def __init__(self, target_point=None, visible_check=False):
        self.owner = None
        self.target_point = target_point  # targetの位置を格納する
        self.visible_check = visible_check  # 視野に入った場合チェックされ,Trueなら移動する

    @stop_watch
    def take_turn_2(self, target, engine):
        results = []
        monster = self.owner


        # 視野のチェック
        # if monster.is_visible:
        #     self.visible_check = True

        # ターゲット座標の更新
        if target:
            self.target_point = target.x, target.y


        if self.visible_check:
            # engine.damage_pop.append(DamagePop("!", (200,100,0), monster, 15))

            # #playerをtargetにしたダイクストラマップを作成
            engine.target_player_map.compute_distance_map(targets=[target], blocks=engine.cur_level.actor_sprites)

            result_dijkstra = engine.target_player_map.get_low_number(monster.x, monster.y)

            if monster.fighter.skill_list:
                self_skills =  monster.fighter.skill_list
                cur_skill = None
                for s in self_skills:
                    if s.count_time <= 0:
                        cur_skill = s
                        break


                if cur_skill and monster.is_visible:
                    cur_skill.target = target
                    cur_skill.use(engine)
                    return "ok"






                # results[1]がターゲットパスへの最初のタイル座標なので変数pointに格納
                elif result_dijkstra:
                    point = result_dijkstra


                    x, y = point[0], point[1]
                    # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                    dx = x - monster.x
                    dy = y - monster.y

                    # attack = monster.move(
                    #     (dx, dy), target, engine)
                    # if attack:
                    #     results.extend(attack)


                    results.extend([{"action":(self.owner,(dx, dy))}])

            else:
                results.extend([{"turn_end": monster}])


        else:
            results.extend([{"turn_end": monster}])
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


        if self.visible_check:

            result_astar = astar([wall_sprites, actor_sprites], (monster.x, monster.y), (self.target_point))

            # results[1]がターゲットパスへの最初のタイル座標なので変数pointに格納
            if result_astar:
                point = result_astar[1]


                x, y = point[0], point[1]
                # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                dx = x - monster.x
                dy = y - monster.y

                attack = monster.move(
                    (dx, dy), target, engine)
                if attack:
                    results.extend(attack)

            elif not result_astar:
                path = breadth_first_search(engine.square_graph, (self.owner.x, self.owner.y), (target.x, target.y))
                if path:
                    print(path, "path")
                    point = path[-1]
                    x, y = point[0], point[1]
                    # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                    dx = x - monster.x
                    dy = y - monster.y

                    attack = monster.move(
                        (dx, dy), target, engine)
                    if attack:
                        results.extend(attack)

                else:
                    results.extend([{"turn_end": monster}])

            else:
                results.extend([{"turn_end": monster}])


        else:
            results.extend([{"turn_end": monster}])
        return results


    @stop_watch
    def take_turn_2(self, target, engine):
        results = []
        monster = self.owner


        # 視野のチェック
        # if monster.is_visible:
        #     self.visible_check = True

        # ターゲット座標の更新
        if target:
            self.target_point = target.x, target.y


        if self.visible_check:
            # engine.damage_pop.append(DamagePop("!", (200,100,0), monster, 15))

            # #playerをtargetにしたダイクストラマップを作成
            engine.target_player_map.compute_distance_map(targets=[target], blocks=engine.cur_level.actor_sprites)

            result_dijkstra = engine.target_player_map.get_low_number(monster.x, monster.y)


            # results[1]がターゲットパスへの最初のタイル座標なので変数pointに格納
            if result_dijkstra:
                point = result_dijkstra


                x, y = point[0], point[1]
                # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
                dx = x - monster.x
                dy = y - monster.y

                # attack = monster.move(
                #     (dx, dy), target, engine)
                # if attack:
                #     results.extend(attack)

                results.extend([{"action":(self.owner,(dx, dy))}])

            else:
                results.extend([{"turn_end": monster}])


        else:
            results.extend([{"turn_end": monster}])
        return results



def auto_explore(engine, player, tar="floor"):
    results = []
    floor = None
    stairs = None
    # ##test
    if tar == "floor":
        floor = [floor for floor in engine.cur_level.floor_sprites if floor.color == (0,0,0)]
    if floor:
        engine.target_tile_map.compute_distance_map(targets=floor)
    else:
        stairs = [stairs for stairs in engine.cur_level.map_obj_sprites if Tag.down_stairs in stairs.tag]
    if stairs:
        engine.target_tile_map.compute_distance_map(targets=stairs)
    ##
    result_dijkstra = engine.target_tile_map.get_low_number(player.x, player.y)
    if result_dijkstra:
        point = result_dijkstra


        x, y = point[0], point[1]
        # ターゲット座標から自分の座標を引いたdx,dyをmoveに渡す
        dx = x - player.x
        dy = y - player.y

        results.extend([{"action":(player,(dx, dy))}])

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
            results.extend([{"turn_end": monster}])

        return results
