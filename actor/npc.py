# doorと同じ処理でtalkにqueueを投げる
from actor.actor import Actor
from data import *
from constants import *
from actor.ai import RandomMove

class Villager(Actor):
    def __init__(self, x=0, y=0):
        ai_component = RandomMove()

        super().__init__(
            scale=2.5,
            name="villager",
            x=x,
            y=y,
            speed=5,
            ai=ai_component,
            blocks=False
        )
        self.tag = {Tag.npc, Tag.friendly}

        self.message = [
            {"message":"test ABC"} ,{"message":"mock_testtesttest"}
        ]