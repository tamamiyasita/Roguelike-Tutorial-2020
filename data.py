import arcade
from util import get_tile_set

image = {"player": r"image/rou6.png",
         "player_move": r"image/rou6_m.png",
         "test_wall": r"image/wall.png",
         "test_floor": r"image/floor.jpg",
         "crab": r"image/crab.png"



         }
walls_1 = (r"image/wall1.png")
walls_2 = (r"image/wall2.png")
walls_3 = (r"image/wall3.png")

walls_1_tiles = get_tile_set(walls_1, tile_size=16)
print(len(walls_1_tiles))
