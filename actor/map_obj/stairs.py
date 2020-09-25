from constants import *
from actor.actor import Actor


class Stairs(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture_number=31,
            name="stairs",
            x=x,
            y=y,
            scale=SPRITE_SCALE*2,

            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")
        )
        self.tag = {Tag.map_obj, Tag.stairs}
