import arcade
from arcade import texture
from actor.actor import Actor
from data import *
from constants import *


class Wall(Actor):
    def __init__(self, texture_number=0, x=0, y=0):
        super().__init__(
            texture_number=texture_number,
            name="wall_C",
            x=x,
            y=y,
            scale=4,
            blocks=True,
            color=COLORS.get("transparent"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")

        )
        self.alpha = 0


    def set_texture(self, texture_no):
        return super().set_texture(self.texture_number)
