from actor.actor import Actor
from constants import *
from data import IMAGE_ID


class StunStatus(Actor):
    def __init__(self, count_time=None):
        super().__init__(
            image=IMAGE_ID["stun"],
            scale=4.5,

        )

        self.owner = None

        self.count_time = count_time
        self.max_cooldown_time = 4

        self.level = 1
        self.damage = None
        self.attr = "mind"
        self.hit_rate = None
        self.effect = None



        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f""
        self.icon = IMAGE_ID["stun"]

    def apply(self, engine):

        # if self.owner and self.count_time >= 0:

        self.owner.fighter.wait += 15
        print(f"stun! {self.owner.name=} {self.owner.fighter.wait=} {self.owner.fighter.speed=}")

        results = [{"message": f"{self.owner.name} STUN!"}]
        results.append({"damage_pop": self.owner, "damage":"STUN"})
        self.owner.state = state.TURN_END

        return results


    def use(self, target):
        target.fighter.wait += 15
        target.state = state.TURN_END