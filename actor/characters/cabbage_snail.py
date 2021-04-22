from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *
from actor.skills.base_skill import BaseSkill


class CabbageSnail(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=9, STR=1, DEX=1,
                                    speed=9,
                                    defense=2,
                                    evasion=2,
                                    xp_reward=3,
                                    level=1,
                                    resist={"physical": 1, "fire": 1, "ice": 1, "elec":1,
                                             "acid": 1, "poison": 1, "mind": 1}
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=1.8,
            name="cabbage_snail",
            image="cabbage_snail",
            x=x,
            y=y,
            # speed=8,
            ai=ai_component,
            blocks=True
        )
        self.fighter=fighter_component
        self.fighter.owner = self

        self.tag = [Tag.npc, Tag.enemy]


        self.unarmed = BaseSkill()
        self.unarmed.owner = self

