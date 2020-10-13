from actor.actor import Actor
from actor.characters.PC import Player
from actor.items.healing_potion import HealingPotion
from actor.characters.orcs import Orc, Troll
from actor.characters.crab import Crab
from actor.items.short_sword import ShortSword
from actor.items.long_sword import LongSword
from actor.items.small_shield import SmallShield
from actor.items.boomerang import Boomerang
from actor.items.fireball_scroll import FireballScroll, FireballEffect
from actor.items.lightning_scroll import LightningScroll, LightningEffect
from actor.items.confusion_scroll import ConfusionScroll, ConfusionEffect
from actor.items.cirsium import Cirsium
from actor.items.leaf_blade import LeafBlade
from actor.items.ebony import Ebony
from actor.items.branch_baton import BranchBaton
from actor.map_obj.wall import Wall
from actor.map_obj.floor import Floor
from actor.map_obj.stairs import Stairs
from actor.map_obj.door import Door

from util import stop_watch


# @stop_watch
def restore_actor(actor_dict):
    actor_name = list(actor_dict.keys())[0]

    if actor_name == "Actor":
        actor = Actor()
    elif actor_name == "Player":
        actor = Player()

    elif actor_name == "ShortSword":
        actor = ShortSword()
    elif actor_name == "LongSword":
        actor = LongSword()
    elif actor_name == "SmallShield":
        actor = SmallShield()
    elif actor_name == "Boomerang":
        actor = Boomerang()

    elif actor_name == "HealingPotion":
        actor = HealingPotion()
    elif actor_name == "FireballScroll":
        actor = FireballScroll()
    elif actor_name == "FireballEffect":
        actor = FireballEffect()
    elif actor_name == "LightningScroll":
        actor = LightningScroll()
    elif actor_name == "LightningEffect":
        actor = LightningEffect()
    elif actor_name == "ConfusionScroll":
        actor = ConfusionScroll()
    elif actor_name == "ConfusionEffect":
        actor = ConfusionEffect()

    elif actor_name == "Cirsium":
        actor = Cirsium()
    elif actor_name == "Ebony":
        actor = Ebony()
    elif actor_name == "LeafBlade":
        actor = LeafBlade()
    elif actor_name == "BranchBaton":
        actor = BranchBaton()

    elif actor_name == "Orc":
        actor = Orc()
    elif actor_name == "Troll":
        actor = Troll()
    elif actor_name == "Crab":
        actor = Crab()
    elif actor_name == "Wall":
        actor = Wall()
    elif actor_name == "Floor":
        actor = Floor()
    elif actor_name == "Stairs":
        actor = Stairs()
    elif actor_name == "Door":
        actor = Door()
    else:
        raise ValueError(f"Error, don't know how to restore {actor_name}.")

    actor.restore_from_dict(actor_dict[actor_name])

    return actor
