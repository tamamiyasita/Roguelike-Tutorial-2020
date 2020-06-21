import arcade
from random import randint

from map_tool import initialize_tiles, Rect, is_blocked
from map_sprite_set import MapSpriteSet
from util import map_position, pixel_position
from actor import Actor
from constants import *


class BasicDungeon:
    def __init__(self, width, height, max_rooms=MAX_ROOM, room_min_size=ROOM_MIN_SIZE, room_max_size=ROOM_MAX_SIZE):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.tiles = initialize_tiles(self.width, self.height)
        self.player_pos = 0
        self.make_map()

    def make_map(self):

        rooms = []
        num_rooms = 0

        for _ in range(self.max_rooms):
            w = randint(self.room_min_size, self.room_max_size)
            h = randint(self.room_min_size, self.room_max_size)
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    self.player_pos = (new_x, new_y)

                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, new_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        return is_blocked(self.tiles, x, y)

        # try:
        #     if self.tiles[x][y].blocked:
        #         return True

        #     return False
        # except:
        #     pass
