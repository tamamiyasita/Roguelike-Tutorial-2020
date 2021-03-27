# doorと同じ処理でtalkにqueueを投げる
from actor.actor import Actor
from data import *
from constants import *
from actor.ai import RandomMove, Wait
from actor.fighter import Fighter
from actor.skills.healing import Healing
from actor.skills.base_skill import BaseSkill


class Villager(Actor):

    def __init__(self, x=0, y=0):
        fighter_component = Fighter(hp=9, STR=1, DEX=1,
                                    attack_speed=9,
                                    defense=2,
                                    evasion=2,
                                    xp_reward=3,
                                    level=1,
                                    resist={"physical": 1, "fire": 1, "ice": 1, "lightning":1,
                                             "acid": 1, "poison": 1, "mind": 1}
                                    )
        ai_component = RandomMove()

        super().__init__(
            # scale=1.8,
            image="villager",
            x=x,
            y=y,
            # speed=8,
            ai=ai_component,
            blocks=True
        )
        self.fighter=fighter_component
        self.fighter.owner = self

        self.tag = [Tag.npc, Tag.friendly]

        self.message = [
            {"message": "test ABC"}, {"message": "mock_testtesttest"}
        ]


        self.unarmed = BaseSkill()
        self.unarmed.owner = self











class Citizen(Actor):
    def __init__(self, x=0, y=0):
        ai_component = Wait()
        fighter_component = Fighter()
        healing = Healing()
        healing.owner = self
        healing._level = 2


        super().__init__(
            image="citizen",
            x=x,
            y=y,
            # speed=10,
            ai=ai_component,
            blocks=True,
            npc_state=NPC_state.REQUEST
        )
        self.tag = [Tag.npc, Tag.friendly, Tag.quest]
        # self.fighter.skill_list.append(healing)
        self.fighter=fighter_component
        self.fighter.owner = self


        self.message = [
            {"message": "test CDEF"}, {"message": "false_test"}
        ]
        self.message_event = {
                            "request": ["It is a test screen", " for conversation", "Please help me"],
                            "reply":["Yes", "No", "uum...", "See you later"],
                            "waiting":["Then please"],
                            "accepted":["understood"],
                            "reward":["Thank you"],
                            "ok":["Gonna be good"]
                            }
