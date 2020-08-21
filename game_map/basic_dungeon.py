import arcade
from random import randint, choice

from game_map.map_sprite_set import ActorPlacement
from util import pixel_to_grid, grid_to_pixel

from game_map.door_check import door_check
from constants import *
from data import *


MAX_ROOMS = 7
ROOM_MIN_SIZE = 4
ROOM_MAX_SIZE = 8
MAX_MONSTERS_PER_ROOM = 3
MAX_ITEMS_PER_ROOM = 2


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


class BasicDungeon:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.dungeon_level = dungeon_level

        self.tiles = [[TILE.WALL for y in range(height)] for x in range(width)]
        self.actor_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]
        self.item_tiles = [
            [TILE.EMPTY for y in range(height)] for x in range(width)]

        self.player_position = 0
        self.make_map(dungeon_level)

    def make_map(self, dungeon_level):

        rooms = []
        self.num_rooms = 0
        last_room_center_x = None
        last_room_center_y = None

        for _ in range(MAX_ROOMS):
            w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if self.num_rooms == 0:
                    self.player_position = (new_x, new_y)

                else:
                    (prev_x, prev_y) = rooms[self.num_rooms - 1].center()
                    last_room_center_x = new_x
                    last_room_center_y = new_y

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, new_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)

                rooms.append(new_room)

                self.num_rooms += 1

                self.place_entities(
                    room=new_room,
                    dungeon_level=dungeon_level
                )

        self.tiles[last_room_center_x][last_room_center_y] = TILE.STAIRS_DOWN

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y] = TILE.EMPTY

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self.tiles[x][y] == TILE.WALL:
                self.tiles[x][y] = TILE.EMPTY
            if door_check(self.tiles, x-1, y):
                self.tiles[x-1][y] = TILE.DOOR
            if door_check(self.tiles, x+1, y):
                self.tiles[x+1][y] = TILE.DOOR

            else:
                self.tiles[x][y] = TILE.EMPTY

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self.tiles[x][y] == TILE.WALL:
                self.tiles[x][y] = TILE.EMPTY
            if door_check(self.tiles, x, y-1):
                self.tiles[x][y-1] = TILE.DOOR
            if door_check(self.tiles, x, y+1):
                self.tiles[x][y+1] = TILE.DOOR

            else:
                self.tiles[x][y] = TILE.EMPTY

    def place_entities(self, room, dungeon_level):

        if dungeon_level == 1:
            combos = [[], [1], [1, 1], [1, 1, 1], []]
        elif dungeon_level == 2:
            combos = [[], [1, 1], [1, 1, 1], [2], [1, 2]]
        else:
            combos = [[], [1, 1, 1], [2], [1, 2], [1, 1, 2]]
        monster_choice = choice(combos)
        for challenge_level in monster_choice:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not self.actor_tiles[x][y]:
                self.actor_tiles[x][y] = challenge_level

        if dungeon_level == 1:
            combos = [[], [1], [1], [1], []]
        if dungeon_level == 2:
            combos = [[], [1], [], [2], [1]]
        else:
            combos = [[], [1], [2], [1], [1]]
        item_choice = choice(combos)
        for challenge_level in item_choice:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not self.item_tiles[x][y]:
                self.item_tiles[x][y] = challenge_level
