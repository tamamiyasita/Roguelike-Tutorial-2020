import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Orc(Actor):
    def __init__(self, x, y,  game_map=None):
        fighter_component = Fighter(hp=8, defense=1, power=3)
        ai_component = Basicmonster()

        super().__init__(
            name="orc",
            texture=orc_l,
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            map_tile=game_map,
            blocks=True
        )
        self.left_face = False

        ACTOR_LIST.append(self)

    def update_animation(self, delta_time=1 / 60):
        if self.left_face:
            self.texture = orc_l
        else:
            self.texture = orc_r
