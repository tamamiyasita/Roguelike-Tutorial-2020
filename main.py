import arcade
import random
from constants import *
from data import *
from set_map import SetMap
from util import map_position
from actor import Actor


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None
        self.crab = None
        self.actor_list = None
        self.map_tile = None
        self.dist = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.actor_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()

        self.map_tile = SetMap(15, 15, self.map_list)

        self.player = Actor(image["player"], 2, 2, map_tile=self.map_tile)
        self.crab = Actor(image["crab"], 3, 2,
                          scale=0.5, map_tile=self.map_tile)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw()
        self.actor_list.draw()

    def on_update(self, delta_time):

        self.actor_list.update()

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

        self.player.move(self.dist)

        self.crab.move((random.randint(-1, 1), random.randint(-1, 1)))


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
