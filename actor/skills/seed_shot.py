from actor.actor import Actor
from data import *
from constants import *


class SeedShot(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="seed_shot",
            x=x,
            y=y,
            color=COLORS["white"]
        )

        self.damage = 3
        self.hit_rate = 75
        self.speed = 10

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.active, Tag.skill]

        self.explanatory_text = f""


