import arcade
from actor.actor import Actor
from actor.fighter import Fighter
from actor.inventory import Inventory
from data import *
from constants import *
# from util import pixel_to_grid, grid_to_pixel


class Player(Actor):
    def __init__(self,x, y,  game_map=None):
        fighter_component = Fighter(hp=35, defense=3, power=5)
        super().__init__(
            name="player",
            texture=player[0],
            x=x,
            y=y,

            inventory=Inventory(capacity=5),
            fighter=fighter_component,
            map_tile=game_map
        )
        # self.center_x, self.center_y = grid_to_pixel(x, y)
        # self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        self.left_face = False
        # ACTOR_LIST.append(self)

    def update_animation(self, delta_time=1 / 60):
        if self.state == state.ON_MOVE and not self.left_face:
            self.texture = player_move[0]
        if self.state == state.ON_MOVE and self.left_face:
            self.texture = player_move[1]
        if self.state == state.ATTACK and not self.left_face:
            self.texture = player_attack[0]
            # self.texture = self.textures.get("move_left")
        if self.state == state.ATTACK and self.left_face:
            self.texture = player_attack[1]
            # self.texture = self.textures.get("move_right")
        if self.state == state.READY and not self.left_face:
            self.texture = player[0]
        if self.state == state.READY and self.left_face:
            self.texture = player[1]


