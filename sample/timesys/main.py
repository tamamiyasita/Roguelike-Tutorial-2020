import arcade
from constants import *
from set_map import SetMap
from data import *
from util import pixel_to_grid
import random
# from ST import State
from Tick_sys import Ticker
from collections import deque


time_travelers = deque()


class Actor(arcade.Sprite):
    def __init__(self, image, name, center_x, center_y, actor_state, ticker, speed, dist=None, scale=SPRITE_SCALE, map_tile=None):
        super().__init__(image, scale)
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        self.actor_state = actor_state
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        self.map_tile = map_tile
        self.dist = 0
        # self.state = State.TICK

    def take_turn(self):
        r = 0
        if self.name == "crab":
            self.move((-1, -1))
            return self.speed
        # if self.state == State.ENM:
        #     results = [{"go": self}]
        #     QUEUE.extend(results)
        elif self.name == "player":
            if self.dist:
                self.move(self.dist)
                return 45
        return 0

        # return self.speed

    # def do_turn(self):
    #     print("do_turn", self.name)
    #     if self.state == State.ENM:
    #         results = [{"go": self}]
    #         QUEUE.extend(results)
    #     self.ticker.schedule_turn(self.speed, self)

    def move(self, dxy):
        dx, dy = dxy
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)

        if not self.map_tile.is_blocked(self.x + dx, self.y + dy):
            self.center_x += int(dx*SPRITE_SIZE)
            self.center_y += int(dy * SPRITE_SIZE)
            self.dist = 0
            # self.state = State.TICK


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
        self.k = 0

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.actor_list = arcade.SpriteList()
        self.map_list = arcade.SpriteList()

        self.map_tile = SetMap(15, 15, self.map_list)

        self.player = Actor(image["player"], "player", 20, 20,
                            State.PC, self.ticker, 15, map_tile=self.map_tile)
        self.crab = Actor(image["crab"], "crab", 310, 210, State.ENM, self.ticker, 15,
                          scale=0.5, map_tile=self.map_tile)
        self.register(self.crab)
        self.register(self.player)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

    def register(self, obj):
        time_travelers.append(obj)
        obj.action_points = 0

    def release(self, obj):
        time_travelers.remove(obj)

    def tick(self):
        if len(time_travelers) > 0:
            obj = time_travelers[0]
            obj.action_points += obj.speed
            if obj.action_points >= 0:
                # while obj.action_points > 0:
                #     if obj.name == "player":
                #         self.state = State.PC
                #     if obj.take_turn() > 0:
                obj.action_points -= obj.take_turn()
            if obj.action_points <= 0:
                time_travelers.rotate()

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
                action.get("go").move(
                    (random.randint(-1, 1), random.randint(-1, 1)))
                self.state = State.PC
            if "player_go" in action:
                print("ok")
                action.get("player_go").move(self.dist)
                self.dist = 0
                self.state = State.ENM
            if "say" in action:
                action.get("say")
                self.state = State.ENM

        QUEUE = new_queue

    def on_update(self, delta_time):
        # if not self.state == State.PC:

        self.tick()
        # self.state = State.PC

        # self.ticker.ticks += 1
        # self.ticker.next_turn()
        # print(self.state)
        # if QUEUE:
        #     print(QUEUE, "QQQ")
        # self.queue_process()

    def on_key_press(self, key, modifiers):
        # print(self.state, "self.key state")
        # print(QUEUE)
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        # for i in range(10):
        #     self.tick()
            # if self.state == State.PC:
            #     break
        if key == arcade.key.UP:
            self.player.dist = (0, 1)
        if key == arcade.key.DOWN:
            self.player.dist = (0, -1)
        if key == arcade.key.LEFT:
            self.player.dist = (-1, 0)
        if key == arcade.key.RIGHT:
            self.player.dist = (1, 0)
            # self.state = State.ENM
        # if self.dist:
        #     self.player.move(self.dist)
        #     results = [{"player_go": self.player}]
        #     QUEUE.extend(results)

        # if key == arcade.key.A:
        #     results = [{"say": self.say()}]
        #     QUEUE.extend(results)


def say(self):
    print(f"says afrdrlsfr")
    self.player.state = State.TICK


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

