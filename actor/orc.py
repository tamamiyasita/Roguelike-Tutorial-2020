import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Orc(Actor):
    def __init__(self, x=0, y=0,  game_engine=None):
        fighter_component = Fighter(hp=8, defense=1, power=3)
        ai_component = Basicmonster()

        super().__init__(
            name="orc",
            texture="orc",
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )
        self.left_face = False

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = orc[0]
        else:
            self.texture = orc[1]
