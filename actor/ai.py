import arcade
from random import randint
from astar import astar
from constants import *


class Basicmonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, sprite_lists):
        print("???")
        results = []
        print(self.owner)

        monster = self.owner
        print(monster.name, "MN")
        if monster.is_visible and not monster.is_dead:
            actor_list = sprite_lists[1]

            if monster.distance_to(target) >= 1:
                results = astar(
                    sprite_lists, (monster.x, monster.y), (target.x, target.y))
                # print(
                #     f"Path from ({monster.x},{monster.y}) to {target.x},{target.y}", results)
                # monster.move_towards(target.x, target.y, sprite_lists)
                # monster.move((randint(-1, 1), randint(-1, 1)))
                print("results?", results)
                if results:
                    point = results[1]
                    x, y = point
                    dx = x - monster.x
                    dy = y - monster.y
                    print(
                        f"{x}{y}{dx}{dy}, : {monster.x}{monster.y}, {target.name}")

                    attack = monster.move(
                        (dx, dy), target, actor_list, game_map)
                    if attack:
                        results.extend(attack)
            return results

        else:
            results.append({"pass": monster})


class ConfusedMonster:
    def __init__(self, pre_ai, number_of_turns=10):
        self.pre_ai = pre_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, game_map, sprite_lists):
        results = []
        monster = self.owner

        if self.number_of_turns > 0:
            attack = monster.move((randint(-1, 1), randint(-1, 1)))
            if attack:
                results.extend(attack)

            self.number_of_turns -= 1

        else:
            monster.ai = self.pre_ai
            results.append(
                {"message": f"The {monster.name} is no longer confused"})

        return results
