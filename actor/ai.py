import arcade
from random import randint
from astar import astar
from constants import *


class Basicmonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, sprite_lists):
        results = []

        monster = self.owner
        if monster.is_visible and not monster.is_dead:
            actor_list = sprite_lists[0]

            if monster.distance_to(target) >= 1:
                results = astar(
                    sprite_lists, (monster.x, monster.y), (target.x, target.y))
                # print(
                #     f"Path from ({monster.x},{monster.y}) to {target.x},{target.y}", results)
                # monster.move_towards(target.x, target.y, sprite_lists)
                # monster.move((randint(-1, 1), randint(-1, 1)))
                if results:
                    point = results[1]
                    x, y = point
                    dx = x - monster.x
                    dy = y - monster.y

                    attack = monster.move(
                        (dx, dy), target, actor_list, game_map)
                    if attack:
                        results.extend(attack)
            return results

        else:
            results.append({"pass": monster})


class ConfusedMonster:
    def __init__(self, pre_ai, confused_turn=10):
        self.pre_ai = pre_ai
        self.confused_turn = confused_turn

    def take_turn(self, target, game_map, sprite_lists):
        results = []
        monster = self.owner
        actor_list = sprite_lists[0]

        if self.confused_turn > 0:
            attack = monster.move(
                (randint(-1, 1), randint(-1, 1)), None, actor_list, game_map)
            if attack:
                results.extend(attack)

            self.confused_turn -= 1

        else:
            monster.ai = self.pre_ai
            results.append(
                {"message": f"The {monster.name} is no longer confused"})

        return results
