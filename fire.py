import imp

import math
from actor.actor import Actor


class Fire:
    def __init__(self, engine, shooter):
        self.shooter = shooter
        self.x, self.y = self.shooter.x, self.shooter.y
        self.target = None
        self.amm = None
        self.effect_sprites = engine.cur_level.effect_sprites
        self.actor_sprites = engine.cur_level.actor_sprites
        self.trigger = False

    # def update(self):
    #     if self.trigger:

    def shot(self):
        amm = self.shooter.equipment.item_slot["ranged_weapon"]
        self.target = None
        target_distance = None
        results = []

        if not amm:
            results.append({"message": f"You don't have a shooting weapon"})
            return results

        for actor in self.actor_sprites:
            if actor.is_visible and actor.fighter and not actor.is_dead and actor.ai:
                x1, y1 = self.shooter.x, self.shooter.y
                x2, y2 = actor.x, actor.y
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if self.target is None or distance < target_distance:
                    self.target = actor
                    target_distance = distance
                    self.trigger = True

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} shot {self.target.name}"})
            results.extend(self.target.fighter.attack(
                target=self.target, ranged=True))
            results.extend([{"turn_end": self.shooter}])
            self.effect_sprites.append(self)

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results
