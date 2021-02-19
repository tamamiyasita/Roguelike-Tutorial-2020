from constants import TMP_EFFECT_SPRITES
import arcade
from particle import AttackParticle


def hit_particle(target, anime=None):
    for i in range(5):
        particle = AttackParticle()
        particle.position = (target.center_x, target.center_y)
        TMP_EFFECT_SPRITES.append(particle)


class Hit_Anime(arcade.Sprite):
    def __init__(self, texture_list, motion="default", position=None, scale=4):
        super().__init__()

        self.current_texture = 0
        self.position = position
        self.textures = texture_list
        self.texture = texture_list[0]
        self.motion = motion
        self.scale = scale
        self.timer = 0
        TMP_EFFECT_SPRITES.append(self)
        self.update_animation()

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        if self.motion == "default":
            self.timer += delta_time
            if self.timer >= 0.04:

                self.current_texture += 1
                if self.current_texture < len(self.textures):
                    self.set_texture(self.current_texture)
                    self.timer = 0
                else:
                    self.remove_from_sprite_lists()


class Fall(arcade.Sprite):
    def __init__(self, owner, scale=2):
        super().__init__()

        self.current_texture = 0
        self.owner = owner
        self.texture = owner.texture
        self.scale = scale
        self.timer = 0
        self.owner.alpha = 0
        TMP_EFFECT_SPRITES.append(self)
        self.update_animation()

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.timer += delta_time
        self.angle += 10
        if self.angle >= 90:
            self.angle = 90
        if self.timer >= 0.9:
            self.remove_from_sprite_lists()
            self.owner.alpha = 255


