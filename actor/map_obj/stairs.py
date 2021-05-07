from data import IMAGE_ID
from constants import *
from actor.actor import Actor


class Up_Stairs(Actor):
    def __init__(self, x=0, y=0, image=None):
        super().__init__(
            # texture_number=31,
            image=IMAGE_ID["up_stairs"],
            x=x,
            y=y,
            # scale=SPRITE_SCALE*2,

            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")
        )
        self.tag = [Tag.map_obj, Tag.up_stairs]

class Down_Stairs(Actor):
    def __init__(self, x=0, y=0, image=None):
        super().__init__(
            # texture_number=31,
            image=IMAGE_ID["down_stairs"],
            x=x,
            y=y,
            # scale=SPRITE_SCALE*2,

            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")
        )
        self.tag = [Tag.map_obj, Tag.down_stairs]
