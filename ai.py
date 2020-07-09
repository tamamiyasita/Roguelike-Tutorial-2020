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

                    attack = monster.move((dx, dy), target)
                    if attack:
                        results.extend(attack)
        return results


a = Basicmonster()
print()
