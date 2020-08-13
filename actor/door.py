from constants import *
from actor.actor import Actor


class Door(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            texture_number=0,
            name="door",
            scale=4,
            x=x,
            y=y,
            color=COLORS.get("transparent"),
            visible_color=COLORS.get("light_wall"),
            not_visible_color=COLORS.get("dark_wall")
        )
        self.alpha = 0
