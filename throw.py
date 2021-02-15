from data import *
from constants import *
from util import grid_to_pixel
from actor.actor import Actor
from explosion import Explosion


import math
from fire import Fire




class Flying(Actor):
    def __init__(self, shooter, target, engine, amm, particle_num=5):
        super().__init__(
            name=amm.amm,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.target = target
        self.amm = amm
        self.particle_num = particle_num
        self.effect_sprites = self.engine.tmp_effect_sprites

        self.shot_speed = amm.speed
        self.shot_damage = -amm.damage
        self.attr = amm.attr
        self.anime_effect = amm.anime

        TMP_EFFECT_SPRITES.append(self)
    
        self.scale = 4

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
            self.angle += 60

            if arcade.check_for_collision(self, self.target):
                self.trigger = None
                self.effect_sprites.remove(self)

                Explosion(self.anime_effect, self.target.position, self.effect_sprites)



                damage = self.circle_range(self.target.x, self.target.y, self.shot_damage)

                self.engine.action_queue.extend([*damage,{"delay": {"time": 0.9, "action": {"turn_end": self.shooter}}}])

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        print(f"{pixel_x}{pixel_y} apply pixel_x_y")
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.engine.cur_level.actor_sprites)

        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                # results.extend(
                #     [{"message": f"{sprite.name} was struck by a fireball for {amount} points."}])
                result = sprite.fighter.skill_process(self.amm)
                if result:
                    results.extend(result)

    def circle_range(self, x, y):
        print("Click!", x, y)
        results = []
        self.apply_damage(x, y, results)

        self.apply_damage(x-1, y-1, results)
        self.apply_damage(x, y-1, results)
        self.apply_damage(x+1, y-1, results)

        self.apply_damage(x-1, y, results)
        self.apply_damage(x+1, y, results)

        self.apply_damage(x-1, y+1, results)
        self.apply_damage(x, y+1, results)
        self.apply_damage(x + 1, y + 1, results)

        self.engine.player.inventory.remove_item(self)

        print(results, "results")
        return results



class Throw(Fire):
    def __init__(self, engine, shooter, skill):
        super().__init__(engine, shooter, skill=skill)
        self.actor_sprites = engine.cur_level.floor_sprites


    def shot(self, x, y):
        results = []

        for actor in self.actor_sprites:
            if actor.x== x and actor.y == y:
                if actor.is_visible:
                    self.target = actor
                    break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} threw {self.skill.name} at the {self.target.name}"})

            if self.shooter == self.engine.player:
                self.engine.player.state = state.THROW

            Flying(shooter=self.shooter, target=self.target,
                        engine=self.engine, amm=self.skill)

            self.skill.data["count_time"] = self.skill.max_cooldown_time


            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results


    
