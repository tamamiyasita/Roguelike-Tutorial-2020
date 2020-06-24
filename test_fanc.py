import arcade
from util import get_tile_set
from actor import Actor
from data import *


def test(image):
    arcade.open_window(300, 300, "test")

    arcade.start_render()

    tst = arcade.Sprite(image.image(), scale=5)
    # tst.texture = image
    tst.draw()

    # image.get(15).draw_scaled(150, 150, scale=5)
    # print(type(image.get(0)), "imagetipe")

    # print(len(image), image)

    arcade.finish_render()

    arcade.run()


if __name__ == "__main__":
    test(wall_1.get(0))
