import random

from basic_dungeon import BasicDungeon
from dmap_dungeon import DmapDungeon
from caves_dungeon import CavesDungeon


def dungeon_select(width, height):

    select = random.randint(1, 3)

    if select == 1:
        return DmapDungeon(width, height)

    elif select == 2:
        return CavesDungeon(width, height)

    else:
        return BasicDungeon(width, height)
