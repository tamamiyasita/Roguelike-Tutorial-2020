from actor.confusion_scroll import ConfusionScroll
import random
import csv
from arcade import load_texture
from actor.actor import Actor
from actor.ai import Basicmonster
from actor.fighter import Fighter
from data import *
from actor.long_sword import LongSword
from actor.short_sword import ShortSword
from actor.small_shield import SmallShield
from actor.healing_potion import HealingPotion
from actor.lightning_scroll import LightningScroll
from actor.fireball_scroll import FireballScroll




def load_entities(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file)
        for actor in reader:
            monsters.append(actor)

    return monsters

entities = load_entities(r"actor/actors.csv")


def get_random_monster_by_challenge(challenge):
    if challenge:
        filtered_monsters = [monster for monster in entities if int(monster["Challenge"]) == challenge]
        if len(filtered_monsters) == 0:
            raise ValueError(f"Error, no entities for challenge level {challenge}.")
        m1 = random.choice(filtered_monsters)
        return m1

item_list = [
            ShortSword(),SmallShield(), LongSword(),LightningScroll(),
            FireballScroll(),ConfusionScroll()
            ]

def get_random_items_by_challenge(challenge):
    if challenge:
        filtered_items = [item for item in item_list if item.challenge() == challenge]
        if len(filtered_items) == 0:
            raise ValueError(f"Error, no entities for challenge level {challenge}.")
        i1 = random.choice(filtered_items)
        return i1

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
