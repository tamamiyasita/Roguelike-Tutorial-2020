
import random
import csv
from arcade import load_texture
from actor.actor import Actor
from actor.ai import Basicmonster
from actor.fighter import Fighter
from constants import *
from data import *
from actor.items.silver_grass import SilverGrass

from actor.characters.orcs import Orc, Troll
from actor.characters.crab import Crab
from actor.characters.rat import Water_vole
from actor.characters.cabbage_snail import CabbageSnail

from level_up_sys import random_flower_gen


def load_entities(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file)
        for actor in reader:
            monsters.append(actor)

    return monsters


entities = load_entities(r"actor/actors.csv")


# def get_random_monster_by_challenge(challenge):
#     if challenge:
#         filtered_monsters = [monster for monster in entities if int(
#             monster["Challenge"]) == challenge]
#         if len(filtered_monsters) == 0:
#             raise ValueError(
#                 f"Error, no entities for challenge level {challenge}.")
#         m1 = random.choice(filtered_monsters)
#         return m1
def get_random_monster_by_challenge(challenge):
    monster_list = [
        Water_vole(), CabbageSnail() #Crab(),# Orc(), Troll()
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


def make_monster_sprite(monster_dict):
    sprite = Actor(image=monster_dict["Name"])

    sprite.name = monster_dict["Name"]
    sprite.ai = Basicmonster()
    sprite.ai.owner = sprite
    sprite.fighter = Fighter()
    sprite.fighter.owner = sprite
    sprite.fighter.hp = int(monster_dict["HP"])
    sprite.fighter.base_max_hp = int(monster_dict["HP"])
    sprite.fighter.base_strength = int(monster_dict["Attack"])
    sprite.fighter.base_defense = int(monster_dict["Defense"])
    sprite.speed = int(monster_dict["SPEED"])
    sprite.fighter.xp_reward = int(monster_dict["XP"])
    sprite.scale = float(monster_dict["scale"])
    sprite.blocks = True
    sprite.state = state.TURN_END
    print(f"Made a {sprite.name}.")
    return sprite
