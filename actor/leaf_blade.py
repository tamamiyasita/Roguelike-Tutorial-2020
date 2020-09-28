import arcade
from data import *
from constants import *
from actor.actor import Actor

class LeafBlade(Actor):
    def __init__(self, x, y):
        super().__init__(
            name="leaf_blade",
            x=x,
            y=y,
            scale=1.4
        )

        self.slot = "main_hand"
        self.states_bonus = {}
        self.attack_damage = (1, 1, 4)
        self.hit_rate = 97

        self.level = 1

        self.tag = {Tag.item, Tag.equip}


        self.item_margin_x = 6.5*SPRITE_SCALE
        self.item_margin_y = 2.5*SPRITE_SCALE
