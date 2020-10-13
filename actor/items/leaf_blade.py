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
        self.states_bonus = {"DEX": 1}
        self.attack_damage = (1, 2, 6)
        self.hit_rate = 95

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill]

        self.explanatory_text = f""

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE
