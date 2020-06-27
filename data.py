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

d_floor = (r"image/Tile.png")

walls_1_tiles = get_tile_set(walls_1, tile_size=16)
wall_1 = {k: walls_1_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_2_tiles = get_tile_set(walls_2, tile_size=16)
wall_2 = {k: walls_2_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_3_tiles = get_tile_set(walls_3, tile_size=16)
wall_3 = {k: walls_3_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}

ds_floor = get_tile_set(d_floor, tile_size=32)
floor_len = len(ds_floor)
floors = {k: ds_floor[v] for k, v in zip(range(floor_len), range(floor_len))}
lname = "tile"
dtile = (r"image/d_tile.tmx")
mtile = arcade.tilemap.read_tmx(dtile)
wlist = arcade.tilemap.process_layer(mtile, lname)
print(wlist[1])
