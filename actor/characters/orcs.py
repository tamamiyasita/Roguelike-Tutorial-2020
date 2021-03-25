from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Orc(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=8, STR=2, DEX=1,
                                    unarmed={"damage":3, "level":1, "attr":"physical", "hit_rate":85},
                                    defense=1,
                                    evasion=1,
                                    xp_reward=5,
                                    level=1
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=2.5,
            image="orc",
            x=x,
            y=y,
            fighter=fighter_component,
            # speed=8,
            ai=ai_component,
            blocks=True
        )
        self.tag = [Tag.npc, Tag.enemy]


class Troll(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=35,  STR=5, DEX=1,
                                    unarmed={"damage":8, "level":2, "attr":"physical","hit_rate":80},
                                    defense=2,
                                    xp_reward=15,
                                    level=2
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=2.6,
            image="troll",
            x=x,
            y=y,
            speed=9,
            fighter=fighter_component,
            ai=ai_component,
            blocks=True
        )
        self.tag = [Tag.npc, Tag.enemy]
