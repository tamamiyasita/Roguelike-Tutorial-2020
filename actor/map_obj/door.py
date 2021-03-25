from constants import *
from actor.actor import Actor


class DoorH(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture_number=0,
            image="door_h",
            x=x,
            y=y,
            scale=SPRITE_SCALE,

            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall"),

            blocks=True,
            left_face=False,
            block_sight=True,

        )
        self.tag = [Tag.map_obj, Tag.door]

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = self.textures[1]
            self.blocks = False
            self.block_sight = False
        else:
            self.texture = self.textures[0]
            self.blocks = True
            self.block_sight = True


class DoorW(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture_number=0,
            image="door_w",
            x=x,
            y=y,
            scale=SPRITE_SCALE,

            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall"),

            blocks=True,
            left_face=False,
            block_sight=True,

        )
        self.tag = [Tag.map_obj, Tag.door]

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = self.textures[1]
            self.blocks = False
            self.block_sight = False
        else:
            self.texture = self.textures[0]
            self.blocks = True
            self.block_sight = True
