from actor.actor import Actor
from data import *
from constants import *
from fire import Fire

class SeedShot(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="seed_shot",
            x=x,
            y=y,
            color=COLORS["white"],
            data={"switch":True,
                  "count_time":0,
                  "cooldown":False}
        )

        self.owner = None

        self.max_cooldown_time = 2

        self.damage = 3
        self.hit_rate = 75
        self.speed = 10

        self.level = 1

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f""

        self.icon = IMAGE_ID["seed_shot_icon"]

    def use(self, engine):

        if self.data["count_time"] <= 0:

            fire = Fire(engine, self.owner, self)
            result = fire.use()



