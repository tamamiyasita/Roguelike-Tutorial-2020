from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Rangid_AI
from data import *
from constants import *
from actor.skills.base_skill import BaseSkill
from actor.skills.fire_arrow import Firearrow


class Goblin_Shaman(Actor):
    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=9, STR=1, DEX=1,
                                    speed=13,
                                    defense=1,
                                    evasion=3,
                                    xp_reward=7,
                                    level=2,
                                    skill_list=[Firearrow()] ,
                                    resist={"physical": 1, "fire": 1, "ice": 1, "elec":1,
                                             "acid": 1, "poison": 1, "mind": 1}
                                    )
                                    
                                    
                                    
        ai_component = Rangid_AI()

        super().__init__(
            scale=1.8,
            name="goblin_shaman",
            image="goblin_shaman",
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

