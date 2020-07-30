import random
import csv
from arcade import load_texture
from actor.actor import Actor
from actor.ai import Basicmonster
from actor.fighter import Fighter
from data import *



def load_entities(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file)
        for actor in reader:
            monsters.append(actor)

    return monsters

entities = load_entities(r"actor/actors.csv")

# def convert_to_restore_dict(monster):
#     converted = {}
#     converted["texture"] = int(monster["texture"])
#     converted["name"] = monster["name"]
#     converted["fighter"] = {
#                             "hp": int(monster["HP"]),
#                             "max_hp": int(monster["HP"]),
#                             "power": int(monster["Attack"]),
#                             "defence": int(monster["Defense"]),
#                             "xp_reward": int(monster["XP"])
#                             }
#     return converted

def get_random_monster_by_challenge(challenge):
    if challenge:
        filtered_monsters = [monster for monster in entities if int(monster["Challenge"]) == challenge]
        if len(filtered_monsters) == 0:
            raise ValueError(f"Error, no entities for challenge level {challenge}.")
        m1 = random.choice(filtered_monsters)
        return m1

def make_monster_sprite(monster_dict):
    sprite = Actor(
        name=monster_dict["Name"],

    )
    sprite.name = monster_dict["Name"]
    sprite.ai = Basicmonster()
    sprite.ai.owner = sprite
    sprite.fighter = Fighter()
    sprite.fighter.owner = sprite
    sprite.fighter.hp = int(monster_dict["HP"])
    sprite.fighter.base_power = int(monster_dict["Attack"])
    sprite.fighter.base_defense = int(monster_dict["Defense"])
    sprite.fighter.xp_reward = int(monster_dict["XP"])
    sprite.blocks = True
    print(f"Made a {sprite.name}.")
    return sprite

# m = get_random_monster_by_challenge(1)
# print(m)