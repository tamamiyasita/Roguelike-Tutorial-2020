import arcade
from random import randint
from util import map_position, pixel_position
from actor import Actor
from data import *


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if not block_sight:
            block_sight = blocked
        self.block_sight = block_sight

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
            )



class SetMap:
    def __init__(self, width, height, sprite_list):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.sprite_list = sprite_list
        self.sprite_set()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):

        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w -1)
            y = randint(0, map_height - h -1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y

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
        for x in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False


    def is_blocked(self, x, y):
        try:
            if self.tiles[x][y].blocked:
                return True

            return False
        except:
            pass

    def sprite_set(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y].blocked:
                    wall = Actor(
                        image.get("test_wall"), x, y)
                    self.sprite_list.append(wall)
                elif not self.tiles[x][y].blocked:
                    floor = Actor(
                        image.get("test_floor"), x, y)
                    self.sprite_list.append(floor)
