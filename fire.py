import arcade
from data import *
from constants import COLORS, Tag

import math
from actor.actor import Actor


class TriggerPull(Actor):
    def __init__(self, shooter, target, engine):
        super().__init__(
            name=shooter.equipment.item_slot["ranged_weapon"].name,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.target = target
        self.effect_sprites = self.engine.cur_level.effect_sprites


        self.amm_speed = 35
        # self.amm_sprite = arcade.Sprite()
        # self.amm_sprite.texture = self.shooter.equipment.item_slot["ranged_weapon"].texture
        # self.amm_sprite.center_x = self.shooter.center_x
        # self.amm_sprite.center_y = self.shooter.center_y

        self.effect_sprites.append(self)

        x_diff = self.target.center_x - self.center_x
        y_diff = self.target.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)
        self.change_x = math.cos(angle) * self.amm_speed
        self.change_y = math.sin(angle) * self.amm_speed
        print(f"amm angle:{self.angle:.2f}")
        self.trigger = True


    def update(self):
        super().update()
        if self.trigger:
            self.angle += 20

            if arcade.check_for_collision(self, self.target):
                self.trigger = None
                self.effect_sprites.remove(self)
                self.engine.action_queue.extend([{"turn_end": self.shooter}])


class Fire:
    def __init__(self, engine, shooter):
        self.engine = engine
        self.shooter = shooter
        self.x, self.y = self.shooter.x, self.shooter.y
        self.target = None
        self.amm = None
        self.effect_sprites = engine.cur_level.effect_sprites
        self.actor_sprites = engine.cur_level.actor_sprites
        self.trigger = None

    def shot(self):
        amm = self.shooter.equipment.item_slot["ranged_weapon"]
        target_distance = None
        results = []

        if not amm:
            results.append({"message": f"You don't have a shooting weapon"})
            return results

        for actor in self.actor_sprites:
            if actor.is_visible and Tag.enemy in actor.tag:
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
            TriggerPull(shooter=self.shooter, target=self.target,
                        engine=self.engine)
            self.trigger = True

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results
