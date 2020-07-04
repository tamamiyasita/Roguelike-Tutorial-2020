import arcade
from random import randint
from astar import astar


class Basicmonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, sprite_lists):
        results = []

        monster = self.owner
        if monster.is_visible:
            # if monster.alpha == 255:

            if monster.distance_to(target) >= 2:
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

                    monster.move((dx, dy))

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results


a = Basicmonster()
print()
