from data import IMAGE_ID
import arcade
from actor.actor import Actor
from constants import *
from data import *

class PoisonStatus(Actor):
    def __init__(self, owner=None, power=None, effect_time=None, sprites=None):
        super(). __init__()
        self.owner = owner
        self.power = power
        self.effect_time = effect_time
        self.sprites = sprites

    def update_animation(self, delta_time: float = 1/60):
        self.owner.angle += 1

    def apply(self):
        self.texture = self.owner.texture
        self.sprites.append(self)
        
        if 0 < self.effect_time:
            result = self.owner.fighter.change_hp(-self.power)
            
            self.owner.color = arcade.color.GREEN

            return [{"apply":self.owner}, {"message":f"You took {self.power} damage from poison"}, *result]

    def call_off(self):
        self.owner.angle = 0
        self.sprites.remove(self)
        self.owner.color = arcade.color.WHITE
        return [{"message":f"The poison has disappeared from your body"}]

    def get_dict(self):
        result = {}

        result["owner"] = self.owner
        result["power"] = self.power
        result["effect_time"] = self.effect_time

        return result

    def restore_from_dict(self, result):
        self.owner = result["owner"]
        self.power = result["power"]
        self.effect_time = result["effect_time"]


