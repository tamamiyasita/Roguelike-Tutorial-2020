import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Troll(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=35, defense=2, str=5,
                                    unarmed_attack=(1, 1, 5),
                                    speed=9,
                                    xp_reward=75
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=2.6,
            name="troll",
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )

    @staticmethod
    def challenge(self):
        return 2
