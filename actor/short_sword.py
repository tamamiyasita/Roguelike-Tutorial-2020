from actor.actor import Actor
from actor.equip import Equippable
from data import *
from constants import *


class ShortSword(Actor):
    def __init__(self, x=0, y=0):
        equippable_component = Equippable("main_hand", power_bonus=3)
        super().__init__(
            name="short_sword",
            x=x,
            y=y,
            scale=1.4,
            equippable=equippable_component
        )

        # self._owner_ship = None

        self.item_margin_x = 13
        self.item_margin_y = 5

    # def update(self):
    #     if self._owner_ship:
    #         self.color = arcade.color.WHITE
    #         self.alpha = 255
    #         x = self.owner_ship.center_x
    #         if self.owner_ship.left_face:
    #             self.left_face = True
    #             self.center_y = self.owner_ship.center_y - self.item_margin_y
    #             self.center_x = x - self.item_margin_x
    #         if self.owner_ship.left_face == False:
    #             self.left_face = False
    #             self.center_y = self.owner_ship.center_y - self.item_margin_y
    #             self.center_x = x + self.item_margin_x

    # @property
    # def owner_ship(self):
    #     return self._owner_ship

    # @owner_ship.setter
    # def owner_ship(self, my):
    #     self._owner_ship = my
    
    # @owner_ship.deleter
    # def owner_ship(self):
    #     self._owner_ship = None


    @staticmethod
    def challenge():
        return 1

