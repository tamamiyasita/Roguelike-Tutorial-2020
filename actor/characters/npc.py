# doorと同じ処理でtalkにqueueを投げる
from actor.actor import Actor
from data import *
from constants import *
from actor.ai import RandomMove, Wait
from actor.fighter import Fighter


class Villager(Actor):
    def __init__(self, x=0, y=0):
        ai_component = RandomMove()
        fighter_component = Fighter()

        super().__init__(
            name="villager",
            x=x,
            y=y,
            speed=15,
            fighter=fighter_component,

            ai=ai_component,
            blocks=True
        )
        self.tag = [Tag.npc, Tag.friendly]

        self.message = [
            {"message": "test ABC"}, {"message": "mock_testtesttest"}
        ]


class Citizen(Actor):
    def __init__(self, x=0, y=0):
        ai_component = Wait()
        fighter_component = Fighter()


        super().__init__(
            name="citizen",
            x=x,
            y=y,
            speed=45,
            ai=ai_component,
            fighter=fighter_component,
            blocks=True,
            npc_state=NPC_state.REQUEST
        )
        self.tag = [Tag.npc, Tag.friendly, Tag.quest]


        self.message = [
            {"message": "test CDEF"}, {"message": "false_test"}
        ]
        self.message_event = {
                            "request": ["I'm worried", "I'm really coming", "Please help me"],
                            "reply":["Yes", "No", "uum...", "See you later"],
                            "waiting":["Then please"],
                            "accepted":["understood"],
                            "reward":["Thank you"],
                            "ok":["Gonna be good"]
                            }
