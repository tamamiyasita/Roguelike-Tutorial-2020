import arcade
from constants import *
from set_map import SetMap
from data import *


class Actor(arcade.Sprite):
    def __init__(self, image, center_x, center_y, scale=SPRITE_SCALE):
        super().__init__(image, scale)
        self.center_x = center_x
        self.center_y = center_y

    def move(self, dxy):
        self.center_x += dxy[0]*SPRITE_SIZE
        self.center_y += dxy[1]*SPRITE_SIZE


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None
        self.actor_list = None
        self.map_tile = None
        self.dist = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.actor_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()

        self.player = Actor(image["player"], 50, 50)
        self.actor_list.append(self.player)
        self.map_tile = SetMap(15, 15, self.map_list)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw()
        self.actor_list.draw()

    def on_update(self, delta_time):
        if self.dist:
            self.player.move(self.dist)
            self.dist = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if key == arcade.key.UP:
            self.dist = (0, 1)
        if key == arcade.key.DOWN:
            self.dist = (0, -1)
        if key == arcade.key.LEFT:
            self.dist = (-1, 0)
        if key == arcade.key.RIGHT:
            self.dist = (1, 0)


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
