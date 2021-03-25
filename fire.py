import arcade
from data import *
from constants import *

import math
from actor.actor import Actor
from particle import AttackParticle

class TriggerPull(Actor):
    def __init__(self, shooter, target, engine, amm):
        super().__init__(
            image=amm.amm,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.target = target
        self.amm = amm
        self.particle_num = 5
        

        self.shot_speed = 25

        TMP_EFFECT_SPRITES.append(self)

        x_diff = self.target.center_x - self.center_x
        y_diff = self.target.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)
        self.change_x = math.cos(angle) * self.shot_speed
        self.change_y = math.sin(angle) * self.shot_speed
        print(f"amm angle:{self.angle:.2f}")
        self.trigger = True

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        result = []
        if self.trigger:

            if arcade.check_for_collision(self, self.target):
                self.trigger = None
                self.effect_sprites.remove(self)

                for _ in range(self.particle_num):
                    particle = AttackParticle()
                    particle.position = (self.target.center_x, self.target.center_y)
                    TMP_EFFECT_SPRITES.append(particle)
                damage = self.target.fighter.skill_process(self.amm)
                result.extend(damage)


                result.extend([{"delay": {"time": 0.3, "action": {"turn_end": self.shooter}}}])
                self.engine.action_queue.extend(result)


class Fire:
    def __init__(self, engine, shooter, skill):
        self.engine = engine
        self.shooter = shooter
        self.skill = skill
        self.x, self.y = shooter.x, shooter.y
        self.target = None
        self.actor_sprites = engine.cur_level.actor_sprites

    def use(self):
        print("use")
        self.engine.game_state = GAME_STATE.SELECT_LOCATION
        self.engine.grid_select_handlers.append(self.shot)
        return None

    def shot(self, x, y):
        results = []


        for actor in self.actor_sprites:
            if actor.x== x and actor.y == y:
                if actor.is_visible and Tag.enemy in actor.tag:
                    self.target = actor
                    break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} shot {self.target.name}"})

            if self.shooter == self.engine.player:
                self.engine.player.form = form.SHOT


            TriggerPull(shooter=self.shooter, target=self.target,
                        engine=self.engine, amm=self.skill)

            self.skill.count_time = self.skill.max_cooldown_time

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results
