from constants import TMP_EFFECT_SPRITES
import arcade
from particle import AttackParticle
from constants import *

def hit_particle(target, anime=None):
    for i in range(5):
        particle = AttackParticle()
        particle.position = (target.center_x, target.center_y)
        TMP_EFFECT_SPRITES.append(particle)

class Hit_Anime(arcade.Sprite):
    def __init__(self, skill, owner=None, scale=4):
        super().__init__()

        self.current_texture = 0
        self.skill = skill
        self.owner = owner
        self.position = owner.position
        self.textures = skill.anime
        self.texture = self.textures[0]
        self.tmp_state = skill.owner.state
        self.scale = scale
        self.timer = 0

        self.anime_type = skill.anime_type
        # self.add_to_anime = None
        # if self.anime_type == "fall":
        #    self.add_to_anime = Fall(self.owner)

        TMP_EFFECT_SPRITES.append(self)

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.timer += delta_time

        if self.anime_type is None:
            if self.timer >= 0.04:

                self.current_texture += 1
                if self.current_texture < len(self.textures):
                    self.set_texture(self.current_texture)
                    self.timer = 0
                else:
                    self.remove_from_sprite_lists()

        if self.anime_type == "fall":
            self.owner.angle = 180
            self.skill.owner.state = state.SMILE
            if self.timer >= 0.035:
                self.current_texture += 1
                if self.current_texture < len(self.textures):
                    self.set_texture(self.current_texture)
                    self.timer = 0
                else:
                    self.alpha = 30
            if self.timer >= 0.25:
                self.owner.angle = 0
                self.skill.owner.state = None
                self.remove_from_sprite_lists()

        elif self.timer >= 0.5:
            self.remove_from_sprite_lists()


class Fall(arcade.Sprite):
    def __init__(self, owner, scale=2):
        super().__init__()

        self.current_texture = 0
        self.owner = owner
        self.texture = owner.texture
        self.scale = scale
        self.timer = 0
        # self.owner.alpha = 0
        self.alpha = 255
        # TMP_EFFECT_SPRITES.append(self)

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.timer += delta_time
        self.owner.angle = 180
        if self.timer >= 0.29:
            self.owner.angle = 0

            # self.remove_from_sprite_lists()
            # self.owner.alpha = 255


