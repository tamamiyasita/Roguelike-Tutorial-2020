import arcade
from arcade import texture
from actor.actor import Actor
from actor.fighter import Fighter
from actor.ai import Basicmonster
# from actor.inventory import Inventory
from data import *
from constants import *
# from util import pixel_to_grid, grid_to_pixel


class Crab(Actor):
    def __init__(self, x, y,  game_map=None):
        fighter_component = Fighter(hp=10, defense=2, power=4)
        ai_component = Basicmonster()
        

        super().__init__(
            name="crab",
            texture=crab[0],
            x=x,
            y=y,
            fighter=fighter_component,
            ai=ai_component,
            map_tile=game_map,
            scale=1,
            blocks =True
            
        )
        
        self.left_face = False

