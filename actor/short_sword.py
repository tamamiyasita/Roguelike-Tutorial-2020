from actor.actor import Actor
from actor.equippable import Equippable
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

        # self._master = None

        self.item_margin_x = 13
        self.item_margin_y = 5

    # def update(self):
    #     if self._master:
    #         self.color = arcade.color.WHITE
    #         self.alpha = 255
    #         x = self.master.center_x
    #         if self.master.left_face:
    #             self.left_face = True
    #             self.center_y = self.master.center_y - self.item_margin_y
    #             self.center_x = x - self.item_margin_x
    #         if self.master.left_face == False:
    #             self.left_face = False
    #             self.center_y = self.master.center_y - self.item_margin_y
    #             self.center_x = x + self.item_margin_x

    # @property
    # def master(self):
    #     return self._master

    # @master.setter
    # def master(self, my):
    #     self._master = my
    
    # @master.deleter
    # def master(self):
    #     self._master = None


    @staticmethod
    def challenge():
        return 1

