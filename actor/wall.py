import arcade
from arcade import texture
from actor.actor import Actor
from data import *
from constants import *


class Wall(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture="wall_C",
            x=x,
            y=y,
            scale=4,
            blocks=True,
            color=arcade.color.BLACK,
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")

        )
        self.alpha = 0

        MAP_LIST.append(self)

    def set_texture(self, texture_no):
        return super().set_texture(texture_no)
