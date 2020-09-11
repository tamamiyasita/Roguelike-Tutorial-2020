import arcade
from data import *

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
        self.trigger = None
        self.amm_sprite = arcade.Sprite()
        self.amm_speed = 10

    def update(self):
        if self.trigger:
            if arcade.check_for_collision(self.amm_sprite, self.target):
                self.trigger = None
                self.effect_sprites.remove(self.amm_sprite)

    def trigger_pull(self):
        self.amm_sprite.texture = self.shooter.equipment.item_slot["ranged_weapon"].texture
        self.amm_sprite.center_x = self.shooter.center_x
        self.amm_sprite.center_y = self.shooter.center_y
        x_diff = self.target.center_x - self.amm_sprite.center_x
        y_diff = self.target.center_y - self.amm_sprite.center_y
        angle = math.atan2(y_diff, x_diff)

        self.amm_sprite.angle = math.degrees(angle)
        print(f"amm angle:{self.amm_sprite.angle:.2f}")
        self.amm_sprite.change_x = math.cos(angle) * self.amm_speed
        self.amm_sprite.change_y = math.sin(angle) * self.amm_speed

        self.effect_sprites.append(self.amm_sprite)

    def shot(self):
        amm = self.shooter.equipment.item_slot["ranged_weapon"]
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
                    break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} shot {self.target.name}"})
            results.extend(self.shooter.fighter.attack(
                target=self.target, ranged=True))
            results.extend([{"turn_end": self.shooter}])
            self.trigger_pull()
            self.trigger = True

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results
