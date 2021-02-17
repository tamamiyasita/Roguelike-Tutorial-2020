from actor.actor import Actor
from constants import *
from data import *


class StunStatus(Actor):
    def __init__(self, count_time=None):
        super().__init__(
            name="stun",
            scale=4.5,

        )

        self.data={"switch":False,
                   "count_time":count_time,
                   "cooldown":False}
        self.max_cooldown_time = 4
        self.owner = None

        self.level = 1
        self.damage = None
        self.attr = "stun"
        self.hit_rate = None
        self.effect = None



        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f""
        self.icon = IMAGE_ID["stun"]

    def apply(self, engine):
        self.engine = engine

        if self.owner and self.data["count_time"] >= 0:

            self.owner.state == state.STUN
            self.owner.wait = self.owner.fighter.attack_speed

            return [{"message": f"{self.owner.name} STUN!"}]