from actor.actor import Actor
from actor.PC import Player
from actor.healing_potion import HealingPotion
from actor.orcs import Orc
from actor.troll import Troll
from actor.crab import Crab
from actor.short_sword import ShortSword
from actor.long_sword import LongSword
from actor.small_shield import SmallShield
from actor.fireball_scroll import FireballScroll, FireballEffect
from actor.lightning_scroll import LightningScroll, LightningEffect
from actor.confusion_scroll import ConfusionScroll, ConfusionEffect
from actor.wall import Wall
from actor.floor import Floor
from actor.stairs import Stairs
from actor.door import Door


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
