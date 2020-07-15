import arcade
from util import get_tile_set

image = {"player": r"image/rou6.png",
         "player_move": r"image/rou6_m.png",
         "test_wall": r"image/wall.png",
         "test_floor": r"image/floor.jpg",
         "crab": r"image/crab.png"
         }
player = arcade.load_texture_pair(image["player"])
player_move = arcade.load_texture_pair(image["player_move"])
pc_attack = arcade.load_texture_pair(r"image/rou6_a.png")
pc_delay = arcade.load_texture_pair(r"image/rou6_d.png")
pc_delay2 = arcade.load_texture_pair(r"image/rou6_d2.png")

crab = arcade.load_texture_pair(image["crab"])


d_floor = (r"image/Tile.png")
ds_floor = get_tile_set(d_floor, tile_size=32)
floor_len = len(ds_floor)
floors = {k: ds_floor[v] for k, v in zip(range(floor_len), range(floor_len))}


walls_1 = (r"image/wall1.png")
walls_1_tiles = get_tile_set(walls_1, tile_size=16)
wall_1 = {k: walls_1_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_2 = (r"image/wall2.png")
walls_2_tiles = get_tile_set(walls_2, tile_size=16)
wall_2 = {k: walls_2_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_3 = (r"image/wall3.png")
walls_3_tiles = get_tile_set(walls_3, tile_size=16)
wall_3 = {k: walls_3_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}

###items###
d_potion = (r"image/Potion.png")
potion = get_tile_set(d_potion, tile_size=16)

d_scroll = (r"image/Scroll.png")  # 2
scroll = get_tile_set(d_scroll, tile_size=16)

d_effect = (r"image/Effect1.png")  # 83
effect1 = get_tile_set(d_effect, tile_size=16)
#######

###enemys###
d_human1 = (r"image/demi_human1.png")
size = 16
orc_l = arcade.load_texture(
    d_human1, x=0, y=size, width=size, height=size)
orc_r = arcade.load_texture(
    d_human1, x=0, y=size, width=size, height=size, mirrored=True)

torll_l = arcade.load_texture(
    d_human1, x=size*7, y=size, width=size, height=size)
torll_r = arcade.load_texture(
    d_human1, x=size*7, y=size, width=size, height=size, mirrored=True)
#######


class Testimg(arcade.Window):
    def __init__(self):
        size = 16
        super().__init__(100, 100)
        img = arcade.load_texture(
            d_human1, x=0, y=size, width=size, height=size)
        arcade.start_render()
        arcade.draw_texture_rectangle(50, 50, 16, 16, img)


def main():
    test = Testimg()

    arcade.run()


if __name__ == "__main__":
    main()
