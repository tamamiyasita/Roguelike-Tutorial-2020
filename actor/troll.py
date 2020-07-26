import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Troll(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=15, defense=2, power=5, xp_reward=100)
        ai_component = Basicmonster()

        super().__init__(
            name="troll",
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )
        self.left_face = False

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = troll[0]
        else:
            self.texture = troll[1]
