from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Orc(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=8, defense=1, power=2,
                                    unarmed_attack=(1, 1, 3),
                                    xp_reward=35
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=2.5,
            name="orc",
            x=x,
            y=y,
            fighter=fighter_component,
            speed=8,
            ai=ai_component,
            blocks=True
        )

    @staticmethod
    def challenge():
        return 1


class Troll(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=35, defense=2, power=5,
                                    unarmed_attack=(1, 1, 5),
                                    xp_reward=75
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=2.6,
            name="troll",
            x=x,
            y=y,
            speed=9,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )

    @staticmethod
    def challenge():
        return 2
