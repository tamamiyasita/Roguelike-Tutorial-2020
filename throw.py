from data import *
from constants import *
from util import grid_to_pixel
from actor.actor import Actor

import math
from fire import Fire


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        self.current_texture = 0
        self.textures = texture_list
        self.texture = texture_list[0]
        self.scale = 4
        self.timer = 0

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.timer += delta_time
        if self.timer >= 0.04:

            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
                self.timer = 0
            else:
                self.remove_from_sprite_lists()



class Flying(Actor):
    def __init__(self, shooter, target, engine, amm, particle_num=5):
        super().__init__(
            name=amm.name,
            color=COLORS["white"],
        )
        self.engine = engine
        self.center_x = shooter.center_x
        self.center_y = shooter.center_y
        self.shooter = shooter
        self.target = target
        self.particle_num = particle_num
        self.effect_sprites = self.engine.tmp_effect_sprites

        self.shot_speed = amm.speed
        self.shot_damage = -amm.damage
        self.attr = amm.attr
        self.explosion_effect = amm.effect

        self.effect_sprites.append(self)
    
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

                explosion = Explosion(self.explosion_effect)
                explosion.center_x = self.target.center_x
                explosion.center_y = self.target.center_y

                explosion.update_animation()
                self.effect_sprites.append(explosion)


                damage = self.click(self.target.x, self.target.y, self.shot_damage)


                # self.engine.action_queue.extend()
                # if explosion not in self.effect_sprites:
                self.engine.action_queue.extend([*damage,{"delay": {"time": 0.9, "action": {"turn_end": self.shooter}}}])

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        print(f"{pixel_x}{pixel_y} apply pixel_x_y")
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.engine.cur_level.actor_sprites)
        # pc_check = arcade.get_sprites_at_point(
        #     (pixel_x, pixel_y), self.engine.cur_level.chara_sprites)
        # sprites.extend(pc_check)
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                results.extend(
                    [{"message": f"{sprite.name} was struck by a fireball for {amount} points."}])
                result = sprite.fighter.change_hp(amount, self.attr)
                if result:
                    results.extend(result)

    def click(self, x, y, damage):
        print("Click!", x, y)
        results = []
        # FireballEffect(x, y, self.engine.cur_level.effect_sprites)
        self.apply_damage(x, y, damage, results)

        self.apply_damage(x-1, y-1, damage+2, results)
        self.apply_damage(x, y-1, damage+2, results)
        self.apply_damage(x+1, y-1, damage+2, results)

        self.apply_damage(x-1, y, damage+2, results)
        self.apply_damage(x+1, y, damage+2, results)

        self.apply_damage(x-1, y+1, damage+2, results)
        self.apply_damage(x, y+1, damage+2, results)
        self.apply_damage(x + 1, y + 1, damage+2, results)

        self.engine.player.inventory.remove_item(self)

        print(results, "results")
        return results



class Throw(Fire):
    def __init__(self, engine, shooter, amm):
        super().__init__(engine, shooter, amm=amm)

    def shot(self, x, y):
        target_distance = None
        results = []

        for actor in self.actor_sprites:
            if actor.x== x and actor.y == y:
                if actor.is_visible:
                    x1, y1 = self.shooter.x, self.shooter.y
                    x2, y2 = actor.x, actor.y
                    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 )
                    # if self.target is None or distance < target_distance:
                    self.target = actor
                    target_distance = distance
                    break

        if self.target:
            results.append(
                {"message": f"{self.shooter.name} threw {self.amm.name} at the {self.target.name}"})

            if self.shooter == self.engine.player:
                self.engine.player.state = state.THROW

            Flying(shooter=self.shooter, target=self.target,
                        engine=self.engine, amm=self.amm)
            self.trigger = True

            self.amm.data["count_time"] = self.amm.max_cooldown_time

            return results

        else:
            results.extend([{"message": "not enemy"}])

        return results


    
