
import random
import csv
from arcade import load_texture
from actor.actor import Actor
from actor.ai import Basicmonster
from actor.fighter import Fighter
from constants import *
from data import *
from actor.flowers.silver_grass import SilverGrass

from actor.characters.orcs import Orc, Troll
from actor.characters.crab import Crab
from actor.characters.rat import Water_vole
from actor.characters.cabbage_snail import CabbageSnail
from actor.characters.dog import Dog
from actor.characters.goblin_shaman import Goblin_Shaman

from level_up_sys import random_flower_gen



def get_random_monster_by_challenge(challenge):
    monster_list = [
        Water_vole(), CabbageSnail(), Dog(), Goblin_Shaman()  #Crab(),# Orc(), Troll()
    ]
    if challenge:
        # TODO 普通のfor文にして柔軟性のあるリストに作り変える
        filtered_monsters = [monster for monster in monster_list if monster.fighter.level <= challenge]
        if len(filtered_monsters) == 0:
            raise ValueError(
                f"Error, no entities for challenge level {challenge}.")
        m1 = random.choice(filtered_monsters)
        return m1


def get_random_items_by_challenge(challenge):
    item_list = [SilverGrass()
        
    ]
    if challenge:
        filtered_items = [item for item in item_list if item.level <= challenge]
        if len(filtered_items) == 0:
            raise ValueError(
                f"Error, no entities for challenge level {challenge}.")
        i1 = random.choice(filtered_items)
        random_flower_gen(i1, challenge+5)
        return i1

def drop_system(engine, target):
    """リスト内にtupleでitemと確率をまとめて格納する(item, 50)"""
    if hasattr(target, "drop_item") and target.drop_item:
        for items in target.drop_item:
            item = items[0]
            drop = items[1]#INT(50で50パーのドロップ率)
            chance = random.randint(1, 100)
            if drop >=  chance:
                item.position_xy = target.position_xy
                item.level = target.fighter.level
                engine.cur_level.item_sprites.append(item)
        

