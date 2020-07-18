import arcade
from actor.actor import Actor
from actor.fighter import Fighter
from data import *
from constants import *
# from util import pixel_to_grid, grid_to_pixel


class Player(Actor):
    def __init__(self, x=0, y=0,  game_map=None, inventory=0):
        fighter_component = Fighter(hp=35, defense=3, power=5)
        super().__init__(
            name="player",
            texture="player",

            x=x,
            y=y,


            inventory=inventory,
            fighter=fighter_component,
            map_tile=game_map
        )

        self.left_face = False
        self.state = state.READY
        # ACTOR_LIST.append(self)
        self.delay_time = 3.7

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        if self.state == state.ON_MOVE and not self.left_face:
            self.texture = player_move[0]
        if self.state == state.ON_MOVE and self.left_face:
            self.texture = player_move[1]

        if self.state == state.ATTACK and not self.left_face:
            print(self.dst_tile)
            self.texture = pc_attack[0]
        if self.state == state.ATTACK and self.left_face:
            self.texture = pc_attack[1]

        if self.state == state.READY and not self.left_face:
            self.texture = player[0]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[0]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[0]
            if self.delay_time < 0:
                self.delay_time = 3.7
        if self.state == state.READY and self.left_face:
            self.texture = player[1]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[1]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[1]
            if self.delay_time < 0:
                self.delay_time = 2.7
