import arcade
from arcade import texture
from actor.actor import Actor
from data import IMAGE_ID
from constants import *


class Floor(Actor):
    def __init__(self,image=None, texture_number=0, x=0, y=0):
        super().__init__(
            # texture_number=texture_number,
            image=image,
            texture_number=texture_number,
            x=x,
            y=y,
            scale=SPRITE_SCALE*1,
            blocks=False,
            color=COLORS.get("black"),#(255,255,255,255), #
            visible_color=COLORS.get("light_ground"),
            not_visible_color=COLORS.get("dark_ground")

        )
        self.tag = [Tag.map_obj, Tag.floor]

    def update_animation(self, delta_time: float):
        pass


