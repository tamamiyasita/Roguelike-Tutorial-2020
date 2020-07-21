import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
from data import *
from constants import *


class Crab(Actor):
    def __init__(self, x=0, y=0, game_engine=None):
        fighter_component = Fighter(hp=10, defense=2, power=4)
        ai_component = Basicmonster()

        super().__init__(
            name="crab",
            texture="crab",
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            game_engine=game_engine,
            state=state.TURN_END,

            scale=1,
            blocks=True
        )
        self.left_face = False

    # def update_animation(self, delta_time=1 / 60):
    #     if self.left_face:
    #         self.texture = crab[1]
    #     else:
    #         self.texture = crab[0]
