from actor.actor import Actor
from actor.PC import Player
from actor.healing_potion import HealingPotion
from actor.orc import Orc
from actor.troll import Troll
from actor.Crab import Crab
from actor.fireball_scroll import FireballScroll
from actor.lightning_scroll import LightningScroll
from actor.confusion_scroll import ConfusionScroll
from actor.wall import Wall
from actor.floor import Floor
from actor.stairs import Stairs


def restore_actor(actor_dict):
    actor_name = list(actor_dict.keys())[0]

    if actor_name == "Actor":
        actor = Actor()
    elif actor_name == "Player":
        actor = Player()
    elif actor_name == "HealingPotion":
        actor = HealingPotion()
    elif actor_name == "FireballScroll":
        actor = FireballScroll()
    elif actor_name == "LightningScroll":
        actor = LightningScroll()
    elif actor_name == "ConfusionScroll":
        actor = ConfusionScroll()
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
    else:
        raise ValueError(f"Error, don't know how to restore {actor_name}.")

    actor.restore_from_dict(actor_dict[actor_name])

    return actor
