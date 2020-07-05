import arcade
from random import randint

from map_tool import initialize_tiles, Rect, is_blocked
from map_sprite_set import MapSpriteSet
from util import map_position, pixel_position
from actor import Actor
from constants import *
from data import *
from fighter import Fighter
from ai import Basicmonster
from item import Item


class BasicDungeon:
    def __init__(self, width, height, max_rooms=MAX_ROOM, room_min_size=ROOM_MIN_SIZE,
                 room_max_size=ROOM_MAX_SIZE):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_monsters_per_room = 3
        self.max_items_per_room = 2

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
                self.place_entities(
                    new_room, max_monsters_per_room=self.max_monsters_per_room,
                    max_items_per_room=self.max_items_per_room)

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

    def place_entities(self, room, max_monsters_per_room, max_items_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)
        actor_list = MAP_LIST

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([actor for actor in actor_list if actor.x == x and actor.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=1, power=3)
                    ai_component = Basicmonster()
                    monster = Actor(image=demi_human1[11], name="orc", x=x, y=y, scale=SPRITE_SCALE,
                                    blocks=True, fighter=fighter_component, ai=ai_component, sub_img=False, map_tile=self)
                    print("spown!")
                    ACTOR_LIST.append(monster)

        # for i in range(number_of_items):
        #     x = randint(room.x1 + 1, room.x2 - 1)
        #     y = randint(room.y1 + 1, room.y2 - 1)

        #     if not any([actor for actor in actor_list if actor.x == x and actor.y == y]):
        #         self[x][y].blocked = False
        #         item = Actor(
        #             image=potion[0], x=x, y=y, blocks=False, color=COLORS.get("transparent"), visible_color=COLORS.get(
        #                 "light_ground"), not_visible_color=COLORS.get("dark_ground"))
        #         MAP_LIST.append(item)
