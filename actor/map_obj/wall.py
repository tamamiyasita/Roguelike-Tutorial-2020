from actor.actor import Actor
from data import IMAGE_ID
from constants import *


class Wall(Actor):
    def __init__(self, image, texture_number=0, x=0, y=0):
        super().__init__(
            texture_number=texture_number,
            image=image,
            x=x,
            y=y,
            # scale=SPRITE_SCALE*2,
            blocks=True,
            block_sight = True,
            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")

        )
        self.tag = [Tag.map_obj, Tag.wall]

    def update_animation(self, delta_time: float):
        pass
