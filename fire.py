import arcade
from data import *
from constants import *

import math
from actor.actor import Actor
from particle import AttackParticle

class TriggerPull(Actor):
    def __init__(self, shooter, target, engine, amm, particle_num=5):
        super().__init__(
            name=amm,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.target = target
        self.particle_num = particle_num
        self.effect_sprites = self.engine.tmp_effect_sprites

        self.shot_speed = 25

        self.effect_sprites.append(self)

        x_diff = self.target.center_x - self.center_x
        y_diff = self.target.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)
        self.change_x = math.cos(angle) * self.shot_speed
        self.change_y = math.sin(angle) * self.shot_speed
        print(f"amm angle:{self.angle:.2f}")
        self.trigger = True

    def update(self):
        super().update()
        if self.trigger:
            # self.angle += 20

            if arcade.check_for_collision(self, self.target):
                self.trigger = None
                self.effect_sprites.remove(self)
                for _ in range(self.particle_num):
                    particle = AttackParticle()
                    particle.position = (self.target.center_x, self.target.center_y)
                    self.effect_sprites.append(particle)

                # self.engine.action_queue.extend([{"turn_end": self.shooter}])
                self.engine.action_queue.extend([{"delay": {"time": 0.3, "action": {"turn_end": self.shooter}}}])


class Fire:
    def __init__(self, engine, shooter, amm=None):
        self.engine = engine
        self.shooter = shooter
        self.x, self.y = self.shooter.x, self.shooter.y
        self.target = None
        self.amm = amm
        self.effect_sprites = engine.cur_level.effect_sprites
        self.actor_sprites = engine.cur_level.actor_sprites
        self.trigger = None

    def use(self):
        print("use")
        self.engine.game_state = GAME_STATE.SELECT_LOCATION
        self.engine.grid_select_handlers.append(self.shot)
        return None

    def shot(self, x, y):
        target_distance = None
        results = []

        if not self.amm:
            results.append({"message": f"You don't have a shooting weapon"})
            return results

        for actor in self.actor_sprites:
            if actor.x== x and actor.y == y:
                if actor.is_visible and Tag.enemy in actor.tag:
                    x1, y1 = self.shooter.x, self.shooter.y
                    x2, y2 = actor.x, actor.y
                    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 )
                    if self.target is None or distance < target_distance:
                        self.target = actor
                        target_distance = distance
                        break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} shot {self.target.name}"})
            results.extend(self.shooter.fighter.attack(
                target=self.target, ranged=self.amm))
            TriggerPull(shooter=self.shooter, target=self.target,
                        engine=self.engine, amm=self.amm.name)
            self.trigger = True

            self.amm.count_time = self.amm.max_cooldown_time

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results
