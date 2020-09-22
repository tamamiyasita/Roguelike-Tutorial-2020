# doorと同じ処理でtalkにqueueを投げる
from actor.actor import Actor
from data import *
from constants import *
from actor.ai import RandomMove, Wait


class Villager(Actor):
    def __init__(self, x=0, y=0):
        ai_component = RandomMove()

        super().__init__(
            scale=2.5,
            name="villager",
            x=x,
            y=y,
            speed=15,
            ai=ai_component,
            blocks=True
        )
        self.tag = {Tag.npc, Tag.friendly}

        self.message = [
            {"message": "test ABC"}, {"message": "mock_testtesttest"}
        ]


class Citizen(Actor):
    def __init__(self, x=0, y=0):
        ai_component = Wait()

        super().__init__(
            scale=2.5,
            name="citizen",
            x=x,
            y=y,
            speed=45,
            ai=ai_component,
            blocks=True
        )
        self.tag = {Tag.npc, Tag.friendly}

        self.npc_state = NPC_state.REQUEST

        self.message = [
            {"message": "test CDEF"}, {"message": "false_test"}
        ]
        self.message_event = {
                            "request": ["I'm worried", "I'm really coming", "Please help me"],
                            "reply":["Yes", "No", "uum...", "fumm..."],
                            "waiting":["Then please"],
                            "accepted":["understood"],
                            "reward":["Thank you"],
                            "ok":["Gonna be good"]
                            }
