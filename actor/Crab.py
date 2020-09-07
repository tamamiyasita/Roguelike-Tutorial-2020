from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Crab(Actor):
    def __init__(self, x=0, y=0, game_engine=None):
        fighter_component = Fighter(hp=10, defense=2, strength=4,
                                    unarmed_attack=(2, 1, 3),
                                    xp_reward=35, level=1
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=1,
            name="crab",
            x=x,
            y=y,
            fighter=fighter_component,
            speed=12,
            ai=ai_component,
            blocks=True
        )


