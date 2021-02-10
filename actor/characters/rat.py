from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *
from actor.skills.base_skill import BaseSkill

class Water_vole(Actor):
    def __init__(self, x=0, y=0):
        unarmed_component = BaseSkill()
        fighter_component = Fighter(hp=8, STR=1, DEX=1,
                                    unarmed=unarmed_component,
                                    defense=1,
                                    evasion=2,
                                    xp_reward=3,
                                    level=1
                                    )
        ai_component = Basicmonster()

        super().__init__(
            # scale=2.5,
            name="water_vole",
            x=x,
            y=y,
            fighter=fighter_component,
            # speed=8,
            ai=ai_component,
            blocks=True
        )
        self.tag = [Tag.npc, Tag.enemy]

