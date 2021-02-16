from arcade.color import SPRING_BUD
from data import *
from constants import *
from util import grid_to_pixel
from actor.actor import Actor
from hit_anime import Hit_Anime

from damage_range import circle_range
from attack_effect import AttackEffect

import math




class Flying(Actor):
    def __init__(self, shooter, tar_point, engine, skill, spin):
        super().__init__(
            name=skill.amm,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.tar_point = tar_point
        self.skill = skill
        self.spin = spin

        self.shot_speed = skill.speed
        self.delay_time = 10 / skill.speed
        self.shot_damage = -skill.damage
        self.attr = skill.attr
        self.damage_range = skill.damage_range
        self.target = arcade.get_sprites_at_point(self.tar_point.position, self.engine.cur_level.actor_sprites)[0]
        self.attack_effect = AttackEffect(shooter, self.target)

        TMP_EFFECT_SPRITES.append(self)
    
        self.scale = 4
        if hasattr(skill, "amm_scale"):
            self.scale = skill.amm_scale

        x_diff = self.tar_point.center_x - self.center_x
        y_diff = self.tar_point.center_y - self.center_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle)
        self.change_x = math.cos(angle) * self.shot_speed
        self.change_y = math.sin(angle) * self.shot_speed
        print(f"skill angle:{self.angle:.2f}")
        self.trigger = True

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        if self.trigger:
            if self.spin:
                self.angle += self.spin

            if arcade.check_for_collision(self, self.tar_point):
                self.trigger = None
                self.remove_from_sprite_lists()

                # if self.anime_effect:
                if hasattr(self, "anime"):
                    Hit_Anime(self.anime_effect, self.tar_point.position)

                if self.damage_range == "single":
                    damage = self.target.fighter.skill_process(self.skill)
                    self.engine.action_queue.extend([*damage,{"delay": {"time": self.delay_time, "action": {"turn_end": self.shooter}}}])

                    

                elif self.damage_range == "circle":
                    damage = circle_range(self.skill, self.engine, self.tar_point.x, self.tar_point.y)
                    # Hit_Anime(self.anime_effect, self.target.position)
                    self.engine.action_queue.extend([*damage,{"delay": {"time": self.delay_time, "action": {"turn_end": self.shooter}}}])




class Ranged:
    def __init__(self, engine, shooter, skill, spin=None, target=None):
        self.engine = engine
        self.shooter = shooter
        self.skill = skill
        self.x, self.y = shooter.x, shooter.y
        self.actor_sprites = engine.cur_level.floor_sprites


        self.spin = spin
        self.target = target

    def use(self):
        print("use")
        self.engine.game_state = GAME_STATE.SELECT_LOCATION
        self.engine.grid_select_handlers.append(self.shot)
        return None

    def shot(self, x, y):
        results = []
        if not self.target:
            for actor in self.actor_sprites:
                if actor.x== x and actor.y == y:
                    if actor.is_visible:
                        self.target = actor
                        break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} used {self.skill.name}"})

            if self.shooter == self.engine.player:
                self.engine.player.state = self.skill.player_state

            Flying(shooter=self.shooter, tar_point=self.target,
                        engine=self.engine, skill=self.skill, spin=self.spin)

            self.skill.data["count_time"] = self.skill.max_cooldown_time


            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results


    
