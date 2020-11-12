from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE
from util import grid_to_pixel,pixel_to_grid

class TownMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.tiles = [[TILE.EMPTY for y in range(height)] for x in range(width)]
        self.actor_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]
        self.item_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]

    def player_set(self,player):

        self.player = player
        self.player.x, self.player.y = pixel_to_grid(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)