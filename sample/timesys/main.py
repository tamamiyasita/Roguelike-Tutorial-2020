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
        if self.state == State.ENM:
            results = [{"go": self}]
            QUEUE.extend(results)
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
                            State.PC, self.ticker, 15, map_tile=self.map_tile)
        self.crab = Actor(image["crab"], "crab", 310, 210, State.ENM, self.ticker, 15,
                          scale=0.5, map_tile=self.map_tile)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw()
        self.actor_list.draw()

    def queue_process(self):
        global QUEUE
        new_queue = []
        for action in QUEUE:
            print(action)
            if "go" in action:
                print(action.values())
                action.get("go").move((random.randint(-1, 1), random.randint(-1, 1)))
            if "player_go" in action:
                print("ok")
                action.get("player_go").move(self.dist)
                self.dist = 0
            if "say" in action:
                action.get("say")
        QUEUE = new_queue
            
                


    def on_update(self, delta_time):
        self.state = self.player.state
        if self.state == State.TICK:
            self.ticker.ticks += 1
            self.ticker.next_turn()
            print(self.state)
            if QUEUE:
                print(QUEUE,"QQQ")
        self.queue_process()

    def on_key_press(self, key, modifiers):
        if self.state == State.PC:
            print(self.state, "self.key state")
            print(QUEUE)
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
                results = [{"player_go": self.player}]
                QUEUE.extend(results)

            if key == arcade.key.A:
                results = [{"say": self.say()}]
                QUEUE.extend(results)

    def say(self):
        print(f"says afrdrlsfr")
        self.player.state = State.TICK



def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
