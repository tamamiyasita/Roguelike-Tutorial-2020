
from random import randint


def place_entities(room, entities, max_monsters_poer_room):
    number_of_monsters = randint(0, max_monsters_poer_room)

    for i in range(number_of_monsters):
        x = randint(room.x1 + 1, room.x2 - 1)
