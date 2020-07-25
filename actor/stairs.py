import arcade
from constants import *
from actor.actor import Actor


class Stairs(Actor):
    def __init__(self, x, y):
        super().__init__(
            name="stairs",
            x=x,
            y=y,
            color=COLORS.get("transparent"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")
        )
        self.alpha = 0
