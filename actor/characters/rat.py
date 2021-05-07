from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *
from actor.skills.base_skill import BaseSkill
from actor.flowers.aconite import Aconite
from actor.flowers.banana_flower import Bananaflower

class Water_vole(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=8, STR=1, DEX=1,
                                    defense=1,
                                    evasion=2,
                                    xp_reward=3,
                                    level=1,
                                    resist={"physical": 1, "fire": 1, "ice": 1, "elec":1,
                                             "acid": 1, "poison": 1, "mind": 1}
                                    )
        ai_component = Basicmonster()

        super().__init__(
            scale=1.8,
            name="water_vole",
            image="water_vole",
            x=x,
            y=y,
            # speed=8,
            ai=ai_component,
            blocks=True
        )
        self.fighter=fighter_component
        self.fighter.owner = self

        self.tag = [Tag.npc, Tag.enemy]

        self.drop_item = [(Bananaflower(),50), (Aconite(),50)]


        self.unarmed = BaseSkill()
        self.unarmed.owner = self

