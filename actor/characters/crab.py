from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *
from actor.skills.base_skill import BaseSkill


class Crab(Actor):

    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=10, STR=2, DEX=1,
                                    defense=2,
                                    evasion=2,
                                    xp_reward=3,
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


        self.unarmed = BaseSkill(damage=4)
        self.unarmed.owner = self














    # def __init__(self, x=0, y=0):
    #     fighter_component = Fighter(hp=10, STR=4, DEX=2,
    #                                 unarmed={"damage":4, "level":1, "attr":"physical", "hit_rate":95},
    #                                 defense=2,
    #                                 evasion=2,
    #                                 xp_reward=5,
    #                                 level=1
    #                                 )
    #     ai_component = Basicmonster()

    #     super().__init__(
    #         scale=1,
    #         name="crab",
    #         x=x,
    #         y=y,
    #         fighter=fighter_component,
    #         speed=12,
    #         ai=ai_component,
    #         blocks=True
    #     )
    #     self.tag = [Tag.npc, Tag.enemy]
