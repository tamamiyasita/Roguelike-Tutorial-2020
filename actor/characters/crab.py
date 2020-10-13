from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Crab(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=10, STR=4, DEX=2,
                                    unarmed_attack=(2, 1, 3),
                                    hit_rate=95,
                                    defense=2,
                                    evasion=2,
                                    xp_reward=35,
                                    level=1
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
        self.tag = [Tag.npc, Tag.enemy]
