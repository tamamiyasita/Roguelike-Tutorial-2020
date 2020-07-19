import arcade
from arcade import texture
from actor.actor import Actor
from data import *
from constants import *


class Floor(Actor):
    def __init__(self, texture_number=0, x=0, y=0):
        super().__init__(
            texture_number=texture_number,
            texture="floor",
            x=x,
            y=y,
            scale=2,
            blocks=False,
            color=COLORS.get("transparent"),
            visible_color=COLORS.get("light_ground"),
            not_visible_color=COLORS.get("dark_ground")

        )
        self.alpha = 0


    def set_texture(self, texture_no):
        return super().set_texture(texture_no)
