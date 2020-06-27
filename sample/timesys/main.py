import arcade
from constants import *
from set_map import SetMap
from data import *
from util import map_position
import random
# from ST import State
from Tick_sys import Ticker


class Actor(arcade.Sprite):
    def __init__(self, image, name, center_x, center_y, actor_state, ticker, speed, scale=SPRITE_SCALE, map_tile=None):
        super().__init__(image, scale)
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        self.actor_state = actor_state
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        self.map_tile = map_tile
        self.state = State.TICK

    def do_turn(self):
        print("do_turn", self.name)
        self.state = self.actor_state
        self.ticker.schedule_turn(self.speed, self)

    def move(self, dxy):
        dx, dy = dxy
        self.x, self.y = map_position(self.center_x, self.center_y)

        if not self.map_tile.is_blocked(self.x + dx, self.y + dy):
            self.center_x += int(dx*SPRITE_SIZE)
            self.center_y += int(dy * SPRITE_SIZE)
            self.state = State.TICK


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None
        self.crab = None
        self.actor_list = None
        self.map_tile = None
        self.dist = 0
        self.ticker = Ticker()
        self.state = State.PC

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.actor_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()

        self.map_tile = SetMap(15, 15, self.map_list)

        self.player = Actor(image["player"], "player", 20, 20,
                            State.PC, self.ticker, 5, map_tile=self.map_tile)
        self.crab = Actor(image["crab"], "crab", 310, 210, State.ENM, self.ticker, 5,
                          scale=0.5, map_tile=self.map_tile)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw()
        self.actor_list.draw()

    def on_update(self, delta_time):
        self.state = self.player.state
        if self.state == State.TICK:
            self.ticker.ticks += 1
            self.ticker.next_turn()
            for actor in self.actor_list:
                if actor.state == State.PC:
                    self.state = State.PC
                if actor.state == State.ENM:
                    self.state = State.ENM
                    actor.move((random.randint(-1, 1), random.randint(-1, 1)))
            # if self.player.state == State.PC:
            #     self.state = State.PC

            # elif self.crab.state == State.ENM:
            #     self.state = State.ENM
            #     self.crab.move((random.randint(-1, 1), random.randint(-1, 1)))

    def on_key_press(self, key, modifiers):
        if self.state == State.PC:
            print(self.state, "self.key state")
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
            if self.dist:
                self.player.move(self.dist)
                self.dist = 0
            print(self.state)


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
