import arcade
from constants import *
from util import map_position
from set_map import SetMap


pcimg = "rou6.png"


class actor(arcade.Sprite):
    def __init__(self, img, x, y, scale=SPRITE_SCALE):
        super().__init__(scale)
        x, y = map_position(self.center_x, self.center_y)

class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None
        self.actor_list = None
        self.map_tile = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.actor_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()

        self.player = arcade.Sprite(pcimg, center_x=50, center_y=50)
        self.actor_list.append(self.player)
        self.map_tile = SetMap(15, 15, self.map_list)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw()
        self.actor_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
