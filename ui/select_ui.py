import arcade
from constants import *
from util import grid_to_pixel

class SelectUI:
    def __init__(self, engine, viewport_x, viewport_y, sprite_list):
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.sprites = sprite_list
        self.dx, self.dy = engine.player.x, engine.player.y


    def grid_select(self, engine, grid):
        self.dx += grid[0]
        self.dy += grid[1]
        

        self.x, self.y = grid_to_pixel(self.dx, self.dy)

        arcade.draw_rectangle_outline(
            center_x=self.x,
            center_y=self.y,
            width=SPRITE_SIZE*SPRITE_SCALE,
            height=SPRITE_SIZE*SPRITE_SCALE,
            color=arcade.color.LIGHT_BLUE,
            border_width=2
        )