import arcade
from random import randint


class Basicmonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, game_map, sprite_lists):
        results = []

        monster = self.owner
        if monster.is_visible:
            # if monster.alpha == 255:

            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, sprite_lists)
                # monster.move((randint(-1, 1), randint(-1, 1)))

            elif target.fighter.hp > 0:
                print(f"the {monster.name} dance")

        return results


a = Basicmonster()
print()
