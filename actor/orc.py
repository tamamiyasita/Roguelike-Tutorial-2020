from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Orc(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=8, defense=1, power=3, xp_reward=35)
        ai_component = Basicmonster()

        super().__init__(
            name="orc",
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )

