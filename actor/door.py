from constants import *
from actor.actor import Actor


class Door(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture_number=0,
            name="door",
            x=x,
            y=y,
            color=COLORS.get("black"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall"),

            blocks=True,
            block_sight=True,

        )

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = self.textures[1]
            self.blocks = False
            self.block_sight = False
        else:
            self.texture = self.textures[0]
            self.blocks = True
            self.block_sight = True


