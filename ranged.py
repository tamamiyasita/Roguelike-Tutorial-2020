from data import *
from constants import *
from actor.actor import Actor

from damage_range import damage_range, square_shape
from anime.hit_anime import Hit_Anime
from ui.select_ui import SelectUI

import math




class Flying(Actor):
    def __init__(self, shooter, tar_point, engine, skill, spin, range):
        super().__init__(
            image=skill.amm,
            color=COLORS["white"],
        )
        self.engine = engine
        self.select_UI = SelectUI(engine)
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.tar_point = tar_point
        self.skill = skill
        self.spin = spin
        self.range = range

        self.shot_speed = skill.shot_speed
        self.delay_time = 0.6
        self.shot_damage = -skill.damage
        self.attr = skill.attr
        self.damage_range = skill.damage_range
        self.target = arcade.get_sprites_at_point(self.tar_point.position, self.engine.cur_level.actor_sprites)
        if shooter != self.engine.player:
            self.target = arcade.get_sprites_at_point(self.tar_point.position, self.engine.cur_level.chara_sprites)

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
        if self.spin:
            self.angle += self.spin

        if self.trigger:

            if arcade.check_for_collision(self, self.tar_point):
                self.trigger = None
                self.remove_from_sprite_lists()

                if hasattr(self.skill, "anime") and Tag.range_attack in self.skill.tag:
                    Hit_Anime(self.skill, self.tar_point)


                if self.damage_range == "single" and self.target:
                    damage = self.target[0].fighter.skill_process(self.skill)
                    self.engine.action_queue.extend([*damage,{"delay": {"time": self.delay_time, "action": {"turn_end": self.shooter}}}])
                elif self.damage_range == "single" and not self.target:
                    self.engine.action_queue.extend([{"message": "not enemy"}])
                    self.engine.game_state = GAME_STATE.NORMAL
                    self.engine.player.state = state.READY
                    

                else:
                    damage = damage_range(self.skill, self.engine, self.tar_point.position_xy, self.range)
                    self.engine.action_queue.extend([*damage,{"delay": {"time": self.delay_time, "action": {"turn_end": self.shooter}}}])

                self.engine.skill_shape = None




class Ranged:
    def __init__(self, engine, shooter, skill, spin=None, target=None):
        self.engine = engine
        self.shooter = shooter
        self.skill = skill
        self.x, self.y = shooter.x, shooter.y
        self.actor_sprites = engine.cur_level.floor_sprites
        self.range = "single"


        self.spin = spin
        self.target = target

        # ここでスキルの効果範囲を渡す
        if self.skill.damage_range ==  "circle":
            self.range = square_shape(self.skill.size)
            self.engine.skill_shape = self.range
        elif self.range == "single":
            self.range = [(0, 0)]
            self.engine.skill_shape = self.range

    def use(self):
        print("use")
        if self.shooter == self.engine.player:
            self.engine.game_state = GAME_STATE.SELECT_LOCATION
            self.engine.grid_select_handlers.append(self.shot)
            # return None
        else:
            self.engine.action_queue.extend(self.shot(self.target.x, self.target.y))
        return None

    def shot(self, x, y):
        
        results = []
        if not self.target:
            for actor in self.actor_sprites:
                # xyがターゲットの位置と一致するなら
                if actor.x== x and actor.y == y:

                    # ターゲット決定
                    if actor.is_visible:
                        self.target = actor

                        # 左右のスプライトを決める
                        if self.target and self.shooter.x < self.target.x:
                            self.shooter.left_face = False
                        elif self.target and self.shooter.x > self.target.x:
                            self.shooter.left_face = True
                        break

        

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} used {self.skill.name}"})

            if self.shooter == self.engine.player:
                self.engine.player.form = self.skill.player_form

            Flying(shooter=self.shooter, tar_point=self.target,
                        engine=self.engine, skill=self.skill, spin=self.spin, range=self.range)

            self.skill.count_time = self.skill.max_cooldown_time


            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results


    
