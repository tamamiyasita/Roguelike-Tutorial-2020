from actor.actor import Actor
from constants import *
from data import *


class TestHead(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="leaf_blade",
            x=x,
            y=y,
            color=COLORS["white"]
        )

        self.slot = "head"
        self.attack_damage = 5
        self.hit_rate = 95
        self.speed = 6

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill, Tag.image_off, Tag.passive]

        

        self.explanatory_text = f"TST head attack speed"
        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE