import arcade
from actor.actor import Actor
from constants import *
from data import *


class LeafBlade(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="leaf_blade",
            x=x,
            y=y,
            color=COLORS["white"]
        )

        self.slot = "main_hand"
        self._attack_damage = [1, 2, 6]
        self.hit_rate = 95

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill]

        self.explanatory_text = f"the test or test and test"
        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE

    @property
    def attack_damage(self):
        if self.master:
            self._attack_damage[0] = self.master.fighter.level // 2
            self._attack_damage[2] = 6 + self.master.fighter.DEX // 3

        return self._attack_damage
