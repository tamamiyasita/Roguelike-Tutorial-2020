from constants import *
from data import *
from actor.skills.seed_shot import SeedShot
from throw import Throw

class Fruit_bomb(SeedShot):
    def __init__(self, x=0, y=0, name="fruit_bomb"):
        super().__init__(
            name=name,
            x=x,
            y=y
            )

        self.max_cooldown_time = 6

        self.damage = 7
        self.hit_rate = 80
        self.speed = 16

        self.icon = IMAGE_ID["fruit_bomb_icon"]
        self.effect = IMAGE_ID["explosion_effect"]



        


    def use(self, engine):

        if self.data["count_time"] <= 0:

            fire = Throw(engine, self.owner, self)
            result = fire.use()

